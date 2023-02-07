package ru.itits.diploma.corporate_search;

import jakarta.servlet.MultipartConfigElement;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.MultipartConfigFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.util.unit.DataSize;

import java.util.concurrent.Executor;

@SpringBootApplication
@EnableAsync
public class CorporateSearchApplication {

    public static void main(String[] args) {
        SpringApplication.run(CorporateSearchApplication.class, args);
    }

    @Bean
    MultipartConfigElement multipartConfigElement() {
        MultipartConfigFactory factory = new MultipartConfigFactory();
        factory.setMaxFileSize(DataSize.parse("1024GB"));
        factory.setMaxRequestSize(DataSize.parse("1024GB"));
        return factory.createMultipartConfig();
    }

    @Bean
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(2);
        executor.setQueueCapacity(500);
        executor.setThreadNamePrefix("Spider-");
        executor.initialize();
        return executor;
    }
}
