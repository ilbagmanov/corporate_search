package ru.itits.diploma.corporate_search.async.spider;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Executor;
import java.util.stream.Collectors;

import jakarta.annotation.PostConstruct;
import jakarta.servlet.ServletContext;
import org.apache.catalina.core.ApplicationContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class AsyncSpiderService {

    private static final Logger logger = LoggerFactory.getLogger(AsyncSpiderService.class);

    private static final Map<String, ReaderSpider> SPIDERS = new HashMap<>();

    static {
        SPIDERS.put(".txt", new TxtReaderSpider());
    }

    @Autowired
    private ServletContext servletContext;

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
            servletContext.
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
            File movedFile = new File(FILES_IN_CHECKING_URL + "/" + file.getName());
            file.renameTo(movedFile);
            String fileName = movedFile.getName();
            servletContext.ge
            String fileType = fileName.substring(fileName.lastIndexOf('.'));
            if (AsyncSpiderService.SPIDERS.containsKey(fileType))
                executor.execute(() -> SPIDERS.get(fileType).read(movedFile));
        } catch (Exception e) {
            logger.error(e.getMessage());
        }
    }
}
