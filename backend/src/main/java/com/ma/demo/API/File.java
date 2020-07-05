package com.ma.demo.API;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
@Getter
@Setter
@Entity
public class File {
    @Id
    @Column(length = 50) public String id;
    @Lob
    @Basic(fetch = FetchType.LAZY) @Column(columnDefinition = "text") public String content;
}
