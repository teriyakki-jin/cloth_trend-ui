package com.example.fashiontrend.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;

@RestController
public class TrendController {

    @GetMapping("/api/style")
    public Map<String, Integer> getStyleTrends() {
        return Map.of(
            "Street", 15,
            "Minimal", 9,
            "Casual", 12,
            "Y2K", 6
        );
    }

    @GetMapping("/api/brand")
    public Map<String, Integer> getBrandTrends() {
        return Map.of(
            "Mango", 8,
            "Joorti", 6,
            "NilbyP", 5,
            "Menasoo", 4
        );
    }

    @GetMapping("/api/price")
    public Map<String, Integer> getPriceTrends() {
        return Map.of(
            "~50,000", 10,
            "50,000~100,000", 14,
            "100,000+", 3
        );
    }
}