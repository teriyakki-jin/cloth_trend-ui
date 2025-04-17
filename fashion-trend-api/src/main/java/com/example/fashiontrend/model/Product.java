package com.example.fashiontrend.model;

import jakarta.persistence.*;

@Entity
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String brand;
    private String name;
    private String price;
    private String style;

    @Column(name = "image_url")  // DB 컬럼명과 맞추기 (imageFile이나 image_file 선택)
    private String imageUrl;

    // ✅ 기본 생성자 (JPA용)
    public Product() {
    }

    // ✅ 전체 생성자
    public Product(Long id, String brand, String name, String price, String style, String imageUrl) {
        this.id = id;
        this.brand = brand;
        this.name = name;
        this.price = price;
        this.style = style;
        this.imageUrl = imageUrl;
    }

    // ✅ Getter
    public Long getId() {
        return id;
    }

    public String getBrand() {
        return brand;
    }

    public String getName() {
        return name;
    }

    public String getPrice() {
        return price;
    }

    public String getStyle() {
        return style;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    // ✅ 필요시 Setter 추가
    public void setBrand(String brand) {
        this.brand = brand;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setPrice(String price) {
        this.price = price;
    }

    public void setStyle(String style) {
        this.style = style;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }
}
