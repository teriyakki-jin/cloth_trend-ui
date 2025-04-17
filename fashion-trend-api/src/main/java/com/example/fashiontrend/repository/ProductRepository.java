package com.example.fashiontrend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.example.fashiontrend.model.Product;

public interface ProductRepository extends JpaRepository<Product, Long> {

}