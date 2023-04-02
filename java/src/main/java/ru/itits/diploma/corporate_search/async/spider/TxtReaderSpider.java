package ru.itits.diploma.corporate_search.async.spider;

import java.io.File;
import java.util.Scanner;

import org.springframework.stereotype.Component;

@Component
public class TxtReaderSpider implements ReaderSpider {


    @Override
    public void read(File file) {
        try {
            Scanner sc = new Scanner(file);
            while (sc.hasNext())
                System.out.println(sc.next());
            File movedFile = new File("FilesChecked" + "/" + file.getName());
            file.renameTo(movedFile);
            System.out.println("Done");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
