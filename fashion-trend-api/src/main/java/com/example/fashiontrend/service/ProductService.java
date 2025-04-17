package com.example.fashiontrend.service;

import com.example.fashiontrend.model.Product;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.stream.Collectors;

import com.example.fashiontrend.model.Product;
import com.example.fashiontrend.repository.ProductRepository;


@Service
public class ProductService {

    @Autowired
    private ProductRepository productRepository;

    public List<Product> findAll() {
        return productRepository.findAll();
    }

    private List<Product> productList = new ArrayList<>();

    @PostConstruct
    public void init() {
        productList.clear();  // ✅ 기존 데이터 리셋

        try (BufferedReader br = new BufferedReader(new InputStreamReader(
                new FileInputStream("wconcept_products.csv"), StandardCharsets.UTF_8))) {

            String line;
            br.readLine(); // header skip
            int id = 0;

            while ((line = br.readLine()) != null) {
                String[] tokens = line.split(",", 5);
                if (tokens.length == 5) {
                    Product product = new Product(
                            (long) id++,
                            tokens[0], tokens[1], tokens[2], tokens[3], tokens[4]
                    );
                    productList.add(product);
                    productRepository.save(product); // ✅ DB에 저장
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    public List<Product> filter(String style, String brand) {
        List<Product> products = productRepository.findAll();
        return products.stream()
                .filter(p -> (style == null || p.getStyle().equalsIgnoreCase(style)))
                .filter(p -> (brand == null || p.getBrand().equalsIgnoreCase(brand)))
                .toList();
    }

    public Set<String> getAllStyles() {
        return productRepository.findAll()
                .stream().map(Product::getStyle)
                .collect(Collectors.toSet());
    }

    public Set<String> getAllBrands() {
        return productRepository.findAll()
                .stream().map(Product::getBrand)
                .collect(Collectors.toSet());
    }


    public Optional<Product> findById(Long id) {
        return productRepository.findById(id);
    }

    public void loadFromCsv() {
        File csvFile = new File("wconcept_products.csv");
        if (!csvFile.exists()) {
            System.out.println(" CSV 파일이 없습니다!");
        } else {
            System.out.println(" CSV 파일 발견!");
        }
        String csvPath = String.valueOf(csvFile); // 프로젝트 루트 기준
        try (BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(csvPath), StandardCharsets.UTF_8))) {
            String line;
            br.readLine(); // skip header
            while ((line = br.readLine()) != null) {
                String[] tokens = line.split(",", 5);
                if (tokens.length == 5) {
                    Product product = new Product(
                            null,                // ID는 자동 생성
                            tokens[0].trim(),    // brand
                            tokens[1].trim(),    // name
                            tokens[2].trim(),    // price
                            tokens[3].trim(),    // style
                            tokens[4].trim()     // imageUrl
                    );
                    productRepository.save(product);
                    System.out.println("✅ 저장됨: " + product.getBrand() + " - " + product.getName());
                }
            }
            System.out.println("📁 CSV 로드 완료!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
