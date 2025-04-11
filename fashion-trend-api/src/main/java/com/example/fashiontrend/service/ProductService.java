package com.example.fashiontrend.service;

import com.example.fashiontrend.model.Product;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

@Service
public class ProductService {

    private List<Product> productList = new ArrayList<>();

    @PostConstruct
    public void init() {
        String csvPath = "wconcept_products.csv"; // 프로젝트 루트 기준
        int id = 0;
        try (BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(csvPath), StandardCharsets.UTF_8))) {
            String line;
            br.readLine(); // skip header
            while ((line = br.readLine()) != null) {
                String[] tokens = line.split(",", 5);
                if (tokens.length == 5) {
                    productList.add(new Product(id++,tokens[0], tokens[1], tokens[2], tokens[3], tokens[4]));
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public List<Product> filter(String style, String brand) {
        return productList.stream()
                .filter(p -> (style == null || p.getStyle().equalsIgnoreCase(style)))
                .filter(p -> (brand == null || p.getBrand().equalsIgnoreCase(brand)))
                .toList();
    }

    public Set<String> getAllStyles() {
        Set<String> styles = new HashSet<>();
        for (Product p : productList) {
            styles.add(p.getStyle());
        }
        return styles;
    }

    public Set<String> getAllBrands() {
        Set<String> brands = new HashSet<>();
        for (Product p : productList) {
            brands.add(p.getBrand());
        }
        return brands;
    }
}
