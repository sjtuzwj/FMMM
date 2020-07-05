package com.ma.demo.API;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;


@Repository
public interface FileRepo extends JpaRepository<File,String>, CrudRepository<File, String> {
    List<File> findAllByIdContaining(String id);
}