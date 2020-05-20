package com.example.falldetection;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.lang.reflect.Method;
import java.nio.charset.Charset;
import java.util.UUID;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;

import android.bluetooth.BluetoothSocket;

import android.util.Log;

public class BluetoothSerialService {
    private static final String TAG = "BluetoothConnectionServ";

    private static final UUID SerialPortServiceClass_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
//            UUID.fromString("8ce255c0-200a-11e0-ac64-0800200c9a66");


    private boolean mAllowInsecureConnections;

    private int mState;


    // Constants that indicate the current connection state
    public static final int STATE_NONE = 0;       // we're doing nothing
    public static final int STATE_CONNECTING = 2; // now initiating an outgoing connection
    public static final int STATE_CONNECTED = 3;  // now connected to a remote device

    private final BluetoothAdapter mBluetoothAdapter;


    private ConnectThread mConnectThread;
    private BluetoothDevice mmDevice;
    private UUID deviceUUID;


    private ConnectedThread mConnectedThread;

    public BluetoothSerialService() {
        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        mState = STATE_NONE;
        mAllowInsecureConnections = true;

    }

    public void setAllowInsecureConnections(boolean secure){
        mAllowInsecureConnections = secure;
    }

    public void connect(BluetoothDevice device){
//        // Cancel any thread attempting to make a connection
        if (mState == STATE_CONNECTING) {
            if (mConnectThread != null) {mConnectThread.cancel(); mConnectThread = null;}
        }

        // Cancel any thread currently running a connection
        if (mConnectedThread != null) {mConnectedThread.cancel(); mConnectedThread = null;}

        // Start the thread to connect with the given device
        mConnectThread = new ConnectThread(device,SerialPortServiceClass_UUID);
        mConnectThread.start();
        setState(STATE_CONNECTING);
 }


    /**
     * This thread runs while attempting to make an outgoing connection
     * with a device. It runs straight through; the connection either
     * succeeds or fails.
     */
    private class ConnectThread extends Thread {
        private BluetoothSocket mmSocket;
        private BluetoothDevice mmDevice;

        public ConnectThread(BluetoothDevice device, UUID uuid) {
            Log.d(TAG, "ConnectThread: started.");
            mmDevice = device;
            deviceUUID = uuid;
            BluetoothSocket tmp = null;

            // Get a BluetoothSocket for a connection with the
            // given BluetoothDevice
            try {
                if ( mAllowInsecureConnections ) {
                    Method method;

                    method = device.getClass().getMethod("createRfcommSocket", new Class[] { int.class } );
                    tmp = (BluetoothSocket) method.invoke(device, 1);
                }
                else {
                    tmp = device.createRfcommSocketToServiceRecord( SerialPortServiceClass_UUID );
                }
            } catch (Exception e) {
                Log.e(TAG, "create() failed", e);
            }
            mmSocket = tmp;
        }

        public void run(){
            BluetoothSocket tmp = null;
            // Always cancel discovery because it will slow down a connection
            mBluetoothAdapter.cancelDiscovery();

            Log.i(TAG, "RUN mConnectThread ");
//
//            // Get a BluetoothSocket for a connection with the
//            // given BluetoothDevice
//            try {
//
//                tmp = mmDevice.createRfcommSocketToServiceRecord(deviceUUID);
//            } catch (IOException e) {
//                Log.e(TAG, "ConnectThread: Could not create InsecureRfcommSocket " + e.getMessage());
//            }
//
//            mmSocket = tmp;
//
//            // Always cancel discovery because it will slow down a connection
//            mBluetoothAdapter.cancelDiscovery();

            // Make a connection to the BluetoothSocket

            try {
                // This is a blocking call and will only return on a
                setState(STATE_CONNECTING);
                // successful connection or an exception
                mmSocket.connect();
                //Send the name of the connected device back to the UI Activity
                setState(STATE_CONNECTED);

                Log.d(TAG, "run: ConnectThread connected.");
            } catch (IOException e) {
                // Close the socket
                setState(STATE_NONE);
                try {
                    mmSocket.close();
                    Log.d(TAG, "run: Closed Socket.");
                } catch (IOException e1) {
                    Log.e(TAG, "mConnectThread: run: Unable to close connection in socket " + e1.getMessage());
                }
//                Log.d(TAG, "run: ConnectThread: Could not connect to UUID: " + MY_UUID_INSECURE );
            }

            //will talk about this in the 3rd video
            connected(mmSocket,mmDevice);
        }
        public void cancel() {
            setState(STATE_NONE);
            try {
                Log.d(TAG, "cancel: Closing Client Socket.");

                mmSocket.close();
            } catch (IOException e) {
                Log.e(TAG, "cancel: close() of mmSocket in Connectthread failed. " + e.getMessage());
            }
        }
    }


    /**
     * Start the chat service. Specifically start AcceptThread to begin a
     * session in listening (server) mode. Called by the Activity onResume()
     */
    public synchronized void start_stop() {
        Log.d(TAG, "start");

        // Cancel any thread attempting to make a connection
        if (mConnectThread != null) {
            mConnectThread.cancel();
            mConnectThread = null;
        }

        setState(STATE_NONE);

    }

    /**
     AcceptThread starts and sits waiting for a connection.
     Then ConnectThread starts and attempts to make a connection with the other devices AcceptThread.
     **/

    public void startClient(BluetoothDevice device,UUID uuid){
        Log.d(TAG, "startClient: Started.");

        mConnectThread = new ConnectThread(device,SerialPortServiceClass_UUID);
        mConnectThread.start();
    }


    /**
     Finally the ConnectedThread which is responsible for maintaining the BTConnection, Sending the data, and
     receiving incoming data through input/output streams respectively.
     **/
    private class ConnectedThread extends Thread {
        private final BluetoothSocket mmSocket;
        private final OutputStream mmOutStream;

        public ConnectedThread(BluetoothSocket socket) {
            Log.d(TAG, "ConnectedThread: Starting.");

            mmSocket = socket;
            OutputStream tmpOut = null;


            try {
                tmpOut = mmSocket.getOutputStream();
                tmpOut.flush();
            } catch (IOException e) {
                e.printStackTrace();
                setState(STATE_NONE);
            }


            mmOutStream = tmpOut;
        }

        //10520 output buffer cache size

        //Call this from the main activity to send data to the remote device
        public void write(byte[] bytes) {
            String text = new String(bytes, Charset.defaultCharset());
            Log.d(TAG, "write: Writing to outputstream: " + text);
            try {
                if (mmOutStream != null)
                    mmOutStream.write(bytes);
                else{

                    connectionFailed();
                    System.out.println("Connection Failed");

                }
            } catch (IOException e) {

                connectionFailed();
                System.out.println("Connection Failed");
                Log.e(TAG, "write: Error writing to output stream. " + e.getMessage() );

            }
        }

        /* Call this from the main activity to shutdown the connection */
        public void cancel() {
            try {
                mmSocket.close();
            } catch (IOException e) { }
        }
    }

    private void connected(BluetoothSocket mmSocket, BluetoothDevice mmDevice) {
        Log.d(TAG, "connected: Starting.");

        // Start the thread to manage the connection and perform transmissions
        mConnectedThread = new ConnectedThread(mmSocket);
        mConnectedThread.start();
    }

    /**
     * Write to the ConnectedThread in an unsynchronized manner
     *
     * @param out The bytes to write
     * @see ConnectedThread#write(byte[])
     */
    public void write(byte[] out) {
        // Create temporary object

        mConnectedThread.write(out);
//        System.out.println("!!!!!");
//        mConnectedThread.cancel();


    }

    /**
     * Set the current state of the chat connection
     * @param state  An integer defining the current connection state
     */
    private synchronized void setState(int state) {
        mState = state;
    }

    /**
     * Return the current connection state. */
    public synchronized int getState() {
        return mState;
    }

    /**
     * Indicate that the connection attempt failed and notify the UI Activity.
     */
    private void connectionFailed() {
        setState(STATE_NONE);
    }

    /**
     * Indicate that the connection was lost and notify the UI Activity.
     */
    private void connectionLost() {
        setState(STATE_NONE);
    }


}
