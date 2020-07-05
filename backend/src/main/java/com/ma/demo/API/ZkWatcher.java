package com.ma.demo.API;

import org.I0Itec.zkclient.ZkClient;

import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.util.List;

public class ZkWactcher{
    protected static final ZkClient zkClient = new ZkClient("172.17.0.3:2181", 5000);
    protected static final String file = "/usr/src/app/host.txt";
    protected static final String host = "/etc/hosts";

    public static void main(String args[]) {
        /*REGISTER*/
        FileReader  fileReader = new FileReader(file);
        BufferedReader bufferedReader = new BufferedReader(fileReader);
        String line =bufferedReader.readLine();
        bufferedReader.close();
        fileReader.close();
        String[] word=line.split(" ");
        zkClient.createPersistent("/host/"+word[1]);
        zkClient.writeData("/host/"+word[1],line);
        /*WATCH*/
        zkClient.subscribeDataChanges(path, new IZkDataListener() {
            @Override
            public void handleDataChange(String dataPath, Object data) throws Exception {
                System.out.println("this program no change");
            }

            @Override
            public void handleDataDeleted(String dataPath) throws Exception {
                System.out.println("this program no delete");
            }
        });
        /*INIT*/
        String res = "";
        List<String> ls = zkClient.getChildren("/host");
        for(String s:ls){
            res = res + zkClient.readData(s);
        }
        FileOutputStream fos = new FileOutputStream(host);
        fos.write(res);
        fos.close();
    }

}
