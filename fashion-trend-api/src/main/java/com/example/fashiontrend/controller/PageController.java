package com.example.fashiontrend.controller;

import com.example.fashiontrend.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import com.example.fashiontrend.model.Product;
import java.util.List;

@Controller
public class PageController {

    private final ProductService productService;

    @Autowired
    public PageController(ProductService productService) {
        this.productService = productService;
    }



    @GetMapping("/gallery")
    public String gallery(@RequestParam(required = false) String style,
                          @RequestParam(required = false) String brand,
                          Model model) {
        model.addAttribute("products", productService.filter(style, brand));
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

}
