package com.example.fashiontrend.controller;

import com.example.fashiontrend.service.ProductService;
import com.example.fashiontrend.service.PythonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import com.example.fashiontrend.model.Product;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.List;

@Controller
public class PageController {

    private final ProductService productService;

    @Autowired
    public PageController(ProductService productService) {
        this.productService = productService;
    }

    @Autowired
    private PythonService pythonService;

    @GetMapping("/gallery")
    public String gallery(@RequestParam(required = false) String style,
                          @RequestParam(required = false) String brand,
                          Model model) {
        List<Product> products = productService.filter(style, brand);
        model.addAttribute("products", products);
        model.addAttribute("styles", productService.getAllStyles());
        model.addAttribute("brands", productService.getAllBrands());
        model.addAttribute("selectedStyle", style);
        model.addAttribute("selectedBrand", brand);
        return "gallery";
    }


    @GetMapping("/product/{id}")
    public String productDetail(@PathVariable int id, Model model) {
        List<Product> all = productService.filter(null, null);
        if (id >= 0 && id < all.size()) {
            model.addAttribute("product", all.get(id));
            return "product_detail";
        }
        return "redirect:/gallery";
    }

    @PostMapping("/search")
    public String search(@RequestParam("keyword") String keyword, Model model) {
        try {
            // 🐍 파이썬 크롤링 실행
            pythonService.runCrawler(keyword);

            // 크롤링 완료 후 CSV 재로딩
            productService.init();

            // 로드한 데이터 모델에 추가
            List<Product> products = productService.findAll();
            model.addAttribute("products", products);
            model.addAttribute("styles", productService.getAllStyles());
            model.addAttribute("brands", productService.getAllBrands());
            model.addAttribute("selectedStyle", null);
            model.addAttribute("selectedBrand", null);

            // ✅ 검색어 유지하고 싶다면 아래도 추가
            model.addAttribute("searchedKeyword", keyword);
            return "gallery";
        } catch (Exception e) {
            e.printStackTrace();
            return "error";
        }


    }


}
