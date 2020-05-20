package com.example.falldetection;

import android.app.Activity;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.renderscript.Matrix4f;

import java.text.DecimalFormat;

public class SensorReader extends Activity implements SensorEventListener {

    private String display_linear_reading;
    private Sensor acceleration,rotation,linear_acceleration;
    private SensorManager SM;
    private final float[] mRotationMatrix = new float[16];
    private  float[] Rotation = new float[3];
    private  float[] Acceleration = new float[3];
    private  float[] Orientation = new float[3];
    private float vx,vy,vz,delta_t;
    private long fall_start_time,fall_end_time;
    private long start_time;
    private Matrix4f mRotation = new Matrix4f();
    private float low_pass_parameter= 0.05f;
    private boolean currently_falling;
    private float initial_free_fall_vy;
    private long system_time;
    public SensorReader(SensorManager sm, Sensor acc,Sensor rot, Sensor lin_acc){

        SM = sm;// Sensor Manager
        acceleration = acc;// Linear Acceleration
        rotation = rot; // Rotation
        linear_acceleration = lin_acc;// Velocity Tracker

        vx= 0f; vy=0f; vz = 0f; //Initializing velocity approximations to zero

        currently_falling = false;

        //Defaults the rotation matrix
        mRotationMatrix[ 0] = 1;
        mRotationMatrix[ 4] = 1;
        mRotationMatrix[ 8] = 1;
        mRotationMatrix[12] = 1;
        mRotation.loadIdentity();

        start_time = System.currentTimeMillis();
        system_time = System.currentTimeMillis();



        // Register sensor Listener
        SM.registerListener(this, acceleration, SensorManager.SENSOR_DELAY_FASTEST);
        SM.registerListener(this, rotation, SensorManager.SENSOR_DELAY_FASTEST);
        SM.registerListener(this, linear_acceleration, SensorManager.SENSOR_DELAY_FASTEST);
    }
    public String Get_display_linear_readings(){

        DecimalFormat df = new DecimalFormat();
        df.setMaximumFractionDigits(2);

        display_linear_reading = "<b>Acceleration:</b><br/>"+
               "X: " + df.format(Acceleration[0])+
               "<br/>Y: " + df.format(Acceleration[1] )+
               "<br/>Z: " + df.format(Acceleration[2] )+

               "<br/>--------------------------------------- <br/>"+
               "<b>Rotation Values:</b><br/>" +
               "Azimuth: " +  df.format(Orientation[0]) +
               "<br/>Pitch: " + df.format(Orientation[1] )+
               "<br/>Roll: " + df.format(Orientation[2] )+
               "<br/>--------------------------------------- <br/>"+

               "<b>Current Velocity:</b><br/>"+
               "X_Vel: "+ ""+ df.format(vx)+
               "<br/>Y_Vel: "+""+ df.format(vy)+
               "<br/>Z_Vel: "+""+ df.format(vz) ;



        return display_linear_reading;
    }

    public String Get_transmit_message(){
        long time_step = (System.currentTimeMillis()-system_time);
        if (currently_falling == true && is_falling()==false){
            //case where it stops falling
            return "##,"+ time_step+","+this.total_height()+","+Orientation[1]+","+Orientation[2]+","+vx+","+vy+","+vz+"\n";

        }
        else if (currently_falling==false && is_falling()==true){
            //case where it begins to fall
            return "**,"+time_step+","+this.is_falling()+","+Orientation[1]+","+Orientation[2]+","+vx+","+vy+","+vz+"\n";
        }

        return "~~,"+ time_step+","+this.is_falling()+"," +Orientation[1]+","+Orientation[2]+","+vx+","+vy+","+vz+"\n";

    }
    public Boolean is_falling(){
        float temp = Acceleration[0]*Acceleration[0]+Acceleration[1]*Acceleration[1]+Acceleration[2]*Acceleration[2];
        if (currently_falling){
            if (temp>96.04){
                currently_falling = false;
                fall_end_time = System.currentTimeMillis();
            }
        }
        else{
            if(temp<3.0){
                if (!currently_falling){
                    initial_free_fall_vy = vy;
                }
                currently_falling = true;
                fall_start_time = System.currentTimeMillis();

            }
        }
        return currently_falling;
    }


    public static boolean almostEqual_toZero(float a, float eps){
        return Math.abs(a)<eps;
    }

    private long fall_duration(){

        return fall_end_time-fall_start_time;
    }

    private float  total_height() {
        double t_fall = (this.fall_duration() * 0.001);
        if (almostEqual_toZero(initial_free_fall_vy, 0.00001f)) {
            // case where phone drops from hand
            return (float) (Math.abs(0.5 * t_fall * t_fall * 9.8));
        } else if (initial_free_fall_vy > 0.0) {
            //case where phone is thrown up
            float t_first = initial_free_fall_vy / 9.8f;
            return (float) (Math.abs(0.5 * Math.pow(t_fall - t_first, 2) * 9.8));
        } else {
            //case where phone is thrown down
            return (float) (Math.abs(initial_free_fall_vy * t_fall + 0.5 * -9.8 * t_fall * t_fall));
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {

        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            // Acceleration Readings
            Acceleration = event.values.clone();

     }
        else if (event.sensor.getType()==Sensor.TYPE_ROTATION_VECTOR){

            //rotation change readings

            SM.getRotationMatrixFromVector(mRotationMatrix ,event.values);
            SM.getOrientation (mRotationMatrix, Orientation);

            Orientation[0] = (float)Math.toDegrees(Orientation[0]);
            Orientation[1] = (float)Math.toDegrees(Orientation[1]);
            Orientation[2] = (float)Math.toDegrees(Orientation[2]);




        }
        else{

            float current_ax = event.values[0];
            float current_ay = event.values[1];
            float current_az = event.values[2];

            long call_time = System.currentTimeMillis();

            delta_t = ((float)(call_time - start_time)) * 0.001f;
            start_time = call_time;

            //Rotates the current phone coordinate readings to global reference frame
            // Note that Global reference == phone when phone is at rotation zero
            float world_ax = mRotationMatrix[0]*current_ax + mRotationMatrix[4]*current_ay + mRotationMatrix[8]*current_az + mRotationMatrix[12];
            float world_ay = mRotationMatrix[1]*current_ax + mRotationMatrix[5]*current_ay + mRotationMatrix[9]*current_az + mRotationMatrix[13];
            float world_az = mRotationMatrix[2]*current_ax + mRotationMatrix[6]*current_ay + mRotationMatrix[10]*current_az + mRotationMatrix[14];



            vx = (world_ax*delta_t)*low_pass_parameter + vx*(1-low_pass_parameter);
            vy = (world_ay*delta_t)*low_pass_parameter + vy*(1-low_pass_parameter);
            vz = (world_az*delta_t)*low_pass_parameter + vz*(1-low_pass_parameter);
        }

    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) { }




}
