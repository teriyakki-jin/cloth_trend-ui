package com.example.fashiontrend.service;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
@Service
public class PythonService {

    public void runCrawler(String keyword) {
        try {
            ProcessBuilder builder = new ProcessBuilder(
                    "python", "src/main/resources/crawler/crawl_wconcept.py", keyword
            );
            builder.redirectErrorStream(true); // 오류도 표준 출력으로
            Process process = builder.start();

            // 로그 출력
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), "UTF-8"));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println("[PYTHON] " + line);
            }

            int exitCode = process.waitFor();
            System.out.println("Python script exited with code: " + exitCode);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
