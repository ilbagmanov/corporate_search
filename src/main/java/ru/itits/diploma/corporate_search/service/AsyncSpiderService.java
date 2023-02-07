package ru.itits.diploma.corporate_search.service;

import com.github.demidko.aot.WordformMeaning;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Scanner;
import java.util.concurrent.Executor;
import java.util.stream.Collectors;

@Service
public class AsyncSpiderService {

    private static final Logger logger = LoggerFactory.getLogger(AsyncSpiderService.class);

    @Autowired
    private Executor executor;

    private final String FILES_NON_CHECKED_URL;
    private final String FILES_IN_CHECKING_URL;
    private final String FILES_CHECKED_URL;

    public AsyncSpiderService(@Value("${spider.files-non-checked-url}") String filesNonCheckedUrl,
                              @Value("${spider.files-in-checking-url}") String filesInCheckingUrl,
                              @Value("${spider.files-checked-url}") String filesCheckedUrl) {
        this.FILES_NON_CHECKED_URL = filesNonCheckedUrl;
        this.FILES_IN_CHECKING_URL = filesInCheckingUrl;
        this.FILES_CHECKED_URL = filesCheckedUrl;
    }

    @PostConstruct
    public void init() {
        executor.execute(this::spiderStarter);
    }

    public void spiderStarter() {
        try {
            cyclicallyCheckFolderForFiles();
        } catch (Exception e) {
            logger.error(e.getMessage());
        }
    }

    private void cyclicallyCheckFolderForFiles() throws Exception {
        while(true) {
            List<Path> filesNonChecked = Files.list(Path.of(FILES_NON_CHECKED_URL)).collect(Collectors.toList());
            if (filesNonChecked.isEmpty())
                logger.info("No files for checking with spider");
            else {
                filesNonChecked.forEach(x -> giveFileToSpider(x.toFile()));
                break;
            }
            Thread.sleep(1000L);
        }
    }

    private void giveFileToSpider(File file) {
        try {
            File movedFile = new File(FILES_IN_CHECKING_URL + "\\" + file.getName());
            file.renameTo(movedFile);
            executor.execute(() -> this.spiderStartUp(movedFile));
        } catch (Exception e) {
            logger.error(e.getMessage());
        }
    }

    private void spiderStartUp(File file) {
        try {
            Scanner scanner = new Scanner(file);
            while (scanner.hasNext()) {
                String word = scanner.next();
                try {
                    var x = WordformMeaning.lookupForMeanings(word);
                    System.out.println(x);
                } catch (Exception e) {
                    System.out.println("ERROR -> " + word);
                }

                System.out.println(word + " ");
            }
            scanner.close();
            file.renameTo(new File(FILES_CHECKED_URL + "\\" + file.getName()));
            logger.info("Complete check file: " + file.getName());
        } catch (Exception e) {
            logger.error(e.getMessage());
        }
    }
}
