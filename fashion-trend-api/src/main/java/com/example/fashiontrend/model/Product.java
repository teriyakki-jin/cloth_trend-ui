package com.example.fashiontrend.model;

public class Product {

    private int id;
    private String brand;
    private String name;
    private String price;
    private String style;
    private String imageUrl;

    public Product(int id, String brand, String name, String price, String style, String imageUrl) {
        this.id = id;
        this.brand = brand;
        this.name = name;
        this.price = price;
        this.style = style;
        this.imageUrl = imageUrl;
    }
    public int getId(){
        return id;
    }

    public String getBrand() { return brand; }
    public String getName() { return name; }
    public String getPrice() { return price; }
    public String getStyle() { return style; }
    public String getImageUrl() { return imageUrl; }
}
