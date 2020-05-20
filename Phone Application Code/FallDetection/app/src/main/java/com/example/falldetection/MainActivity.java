package com.example.falldetection;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;


import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.os.Build;
import android.os.Bundle;

import android.text.Html;

import android.widget.CompoundButton;
import android.widget.TextView;
import android.widget.ToggleButton;

import java.io.IOException;


public class MainActivity extends AppCompatActivity {
    private boolean checked = false;
    private TextView newtext;
    private TextView bluetooth_status;
    private Sensor Accelerometer,Rotationsensor,LinearAcceleration;
    private SensorManager SM;
    private Thread debug_thread;
    private Thread Transmit_thread;
    private SensorReader sensorReader;
    private TransmitData dataSender;
    private int time;
    private boolean done;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Text View used to debug outputs
        newtext = (TextView) findViewById(R.id.textView2);
        ToggleButton toggle = (ToggleButton) findViewById(R.id.toggleButton);
        bluetooth_status = (TextView)findViewById(R.id.textView4);

        //Sensor Manager
        SM = (SensorManager)getSystemService(SENSOR_SERVICE);

        // Rotation Sensor
        Rotationsensor = SM.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR);

        // Acceleration Sensor
        Accelerometer = SM.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);

        // Linear Acceleration i.e w/o gravity
        LinearAcceleration = SM.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);


        sensorReader =  new SensorReader(SM,Accelerometer,Rotationsensor,LinearAcceleration);






        toggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @RequiresApi(api = Build.VERSION_CODES.KITKAT_WATCH)
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                    checked = isChecked;
            }
        });

        Transmit_thread = new Thread(){
            @Override
            public void run() {
                try {
                    done = false;

                    dataSender = new TransmitData();
                    dataSender.start();
                    dataSender.connect_to_pi();
                    time = 500;

                    while (!Transmit_thread.isInterrupted()) {
                        Transmit_thread.sleep(time);
                        dataSender.update_title(bluetooth_status);

                                if (dataSender.connection_status() == 3){
                                    // sends out updated message
                                    //FSystem.out.println("Sending");
                                    dataSender.send(sensorReader.Get_transmit_message());
                                    time= 1000/30;
                                }
                                else{
                                    //tries to re-connect every half second
                                    dataSender.connect_to_pi();
                                    time = 500;

                                }





                    }
                }
                catch (InterruptedException e) { }
            }
        };

        Transmit_thread.start();

        debug_thread = new Thread(){
            @Override
            public void run() {
                try {
                    while (!debug_thread.isInterrupted()) {
                        debug_thread.sleep(50);
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {

                                if (checked)
                                    newtext.setText(Html.fromHtml(sensorReader.Get_display_linear_readings()));


                            }
                        });
                    }
                }
                catch (InterruptedException e) { }
            }
        };

        debug_thread.start();




    }


    @Override
    public void onDestroy() {
        super.onDestroy();
        if (dataSender != null) {
            if (dataSender.connection_status() == 3) {
                //sends out terminate signal to our raspberry pi code
                dataSender.send("e\n");
            }
            dataSender.stop();
        }
    }



}
