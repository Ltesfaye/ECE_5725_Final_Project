package com.example.falldetection;


import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.widget.TextView;

import java.util.Set;

public class TransmitData{
    private BluetoothSerialService bservice;
    public BluetoothAdapter badapter;

    public TransmitData(){

        bservice = new BluetoothSerialService();
        badapter = BluetoothAdapter.getDefaultAdapter();
    }

    public void update_title(TextView mTitle){
        int current_state = bservice.getState();

        if (current_state ==0){
            mTitle.setText("Not Connected!!!");
        }
        else if (current_state ==2){
            mTitle.setText("connecting...");
        }
        else if (current_state ==3){
            mTitle.setText("Connected !!!");
        }
        else{
            mTitle.setText("Searching for connection...");

        }


    }
    public int connection_status(){
        return bservice.getState();
    }

    public void start(){
        bservice.start_stop();
        bservice.setAllowInsecureConnections(true);
    }

    public void connect_to_pi(){
        badapter.startDiscovery();
        Set<BluetoothDevice> bondedDevices = badapter.getBondedDevices();

        String address = null;
        String name = null;

        for (BluetoothDevice device : bondedDevices) {

            address = device.getAddress();
            name  = device.getName();
        }

        System.out.println(name + "~~~" + address+"\n\n");
        BluetoothDevice device = badapter.getRemoteDevice(address);
        bservice.connect(device);
    }

    public void stop(){
        bservice.start_stop();
    }

    public void send(String output){
        if (output.length() > 0){
            bservice.write(output.getBytes());
        }
    }





}