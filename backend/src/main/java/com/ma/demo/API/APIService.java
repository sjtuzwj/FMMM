package com.ma.demo.API;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class APIService {
    @Autowired FileRepo fr;
    void save(File f){
        fr.save(f);
    }
    String get(String id){
        return fr.findById(id).get().content;
    }
    List<File> getLib() {return fr.findAllByIdContaining(
            "lib"
    );}
}
