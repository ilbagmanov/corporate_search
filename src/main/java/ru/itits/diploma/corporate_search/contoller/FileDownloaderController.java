package ru.itits.diploma.corporate_search.contoller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;

@Controller
public class FileDownloaderController {

    @PostMapping(value = "/upload")
    public @ResponseBody
    String handleFileUpload(@RequestParam("file") MultipartFile file) throws Exception {
        if (!file.isEmpty()) {
            byte[] bytes = file.getBytes();
            BufferedOutputStream stream = new BufferedOutputStream(new FileOutputStream("FilesNonChecked\\" + file.getOriginalFilename()));
            stream.write(bytes);
            stream.close();
            return "Вы удачно загрузили " + file.getOriginalFilename();
        } else {
            return "Вам не удалось загрузить " + file.getOriginalFilename() + " потому что файл пустой.";
        }
    }
}
