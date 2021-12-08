package com.example.crc_blutooth;


import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import com.example.crc_blutooth.databinding.ActivityMainBinding;

import android.view.Menu;
import android.view.MenuItem;

import org.jetbrains.annotations.NotNull;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.CertificatePinner;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    private AppBarConfiguration appBarConfiguration;
    private ActivityMainBinding binding;

    TextView mTvBluetoothStatus;
    TextView mTvReceiveData;
    TextView mTvSendData;
    Button mBtnBluetoothOn;
    Button mBtnBluetoothOff;
    Button mBtnConnect;
    Button mBtnSendData;
    ImageView mimageView;
    ImageView msubimageView;

    BluetoothAdapter mBluetoothAdapter;
    Set<BluetoothDevice> mPairedDevices;
    List<String> mListPairedDevices;

    Handler mBluetoothHandler;
    ConnectedBluetoothThread mThreadConnectedBluetooth;
    BluetoothDevice mBluetoothDevice;
    BluetoothSocket mBluetoothSocket;

    final static int BT_REQUEST_ENABLE = 1;
    final static int BT_MESSAGE_READ = 2;
    final static int BT_CONNECTING_STATUS = 3;
    final static UUID BT_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    boolean flag =true;
    boolean click_flag = false;
    boolean second_flag = false;
    String pre_class = "";
    String pre_device_name = "";

    HashMap<String,Integer> imageMap=new HashMap<String,Integer>();


    OkHttpClient client=new OkHttpClient();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mTvBluetoothStatus = (TextView)findViewById(R.id.tvBluetoothStatus);
        mTvReceiveData = (TextView)findViewById(R.id.tvReceiveData);
        mTvSendData =  (EditText) findViewById(R.id.tvSendData);
        mBtnBluetoothOn = (Button)findViewById(R.id.btnBluetoothOn);
        mBtnBluetoothOff = (Button)findViewById(R.id.btnBluetoothOff);
        mBtnConnect = (Button)findViewById(R.id.btnConnect);
        mBtnSendData = (Button)findViewById(R.id.btnSendData);
        mimageView=(ImageView)findViewById(R.id.iv_class);
        msubimageView=(ImageView)findViewById(R.id.iv_sub_class);
        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        /*
        Map Init
        */

        imageMap.put("1",R.drawable.a);
        imageMap.put("2",R.drawable.b);
        imageMap.put("3",R.drawable.c);
        imageMap.put("4",R.drawable.d);
        imageMap.put("5",R.drawable.e);
        imageMap.put("6",R.drawable.f);
        imageMap.put("7",R.drawable.g);
        imageMap.put("8",R.drawable.h);
        imageMap.put("9",R.drawable.i);
        imageMap.put("10",R.drawable.j);
        imageMap.put("11",R.drawable.k);
        imageMap.put("12",R.drawable.l);
        imageMap.put("13",R.drawable.m);
        imageMap.put("14",R.drawable.n);
        imageMap.put("15",R.drawable.o);
        imageMap.put("16",R.drawable.p);
        imageMap.put("-1",R.drawable.blank);

        imageMap.put("1a",R.drawable.a1);
        imageMap.put("1b",R.drawable.b1);
        imageMap.put("1c",R.drawable.c1);
        imageMap.put("2a",R.drawable.a2);
        imageMap.put("2b",R.drawable.b2);
        imageMap.put("2c",R.drawable.c2);
        imageMap.put("3a",R.drawable.a3);
        imageMap.put("3b",R.drawable.b3);
        imageMap.put("3c",R.drawable.c3);
        imageMap.put("4a",R.drawable.a4);
        imageMap.put("4b",R.drawable.b4);
        imageMap.put("4c",R.drawable.c4);
        imageMap.put("5a",R.drawable.a5);
        imageMap.put("5b",R.drawable.b5);
        imageMap.put("5c",R.drawable.c5);
        imageMap.put("6a",R.drawable.a6);
        imageMap.put("6b",R.drawable.b6);
        imageMap.put("6c",R.drawable.c6);
        imageMap.put("7a",R.drawable.a7);
        imageMap.put("7b",R.drawable.b7);
        imageMap.put("7c",R.drawable.c7);
        imageMap.put("8a",R.drawable.a8);
        imageMap.put("8b",R.drawable.b8);
        imageMap.put("8c",R.drawable.c8);
        imageMap.put("9a",R.drawable.a9);
        imageMap.put("9b",R.drawable.b9);
        imageMap.put("9c",R.drawable.c9);
        imageMap.put("10a",R.drawable.a10);
        imageMap.put("10b",R.drawable.b10);
        imageMap.put("10c",R.drawable.c10);
        imageMap.put("11a",R.drawable.a11);
        imageMap.put("11b",R.drawable.b11);
        imageMap.put("11c",R.drawable.c11);
        imageMap.put("13a",R.drawable.a13);
        imageMap.put("13b",R.drawable.b13);
        imageMap.put("13c",R.drawable.c13);
        imageMap.put("15a",R.drawable.a15);
        imageMap.put("15b",R.drawable.b15);
        imageMap.put("15c",R.drawable.c15);







        mBtnBluetoothOn.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                bluetoothOn();
            }
        });
        mBtnBluetoothOff.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                bluetoothOff();
            }
        });
        mBtnConnect.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                listPairedDevices();
            }
        });
        mBtnSendData.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(mThreadConnectedBluetooth != null) {
                    char a = 'a';
                    String ch_a = Character.toString(a);
                    mThreadConnectedBluetooth.write(ch_a);
                    // mThreadConnectedBluetooth.write(mTvSendData.getText().toString());
                    // Log.d("Test","SendData : " + mTvSendData.getText());
                    // mTvSendData.setText("");

                    if(flag && !click_flag) {
                        click_flag = true;
                        flag = true;
                        Toast.makeText(getApplicationContext(), "수화 인식 중", Toast.LENGTH_SHORT).show();
                    }
                    else if(flag && click_flag){
                        flag = false;
                        // click_flag = false;
                        Toast.makeText(getApplicationContext(), "모델 인식 결과", Toast.LENGTH_SHORT).show();
                    }

                }
            }
        });

        mBluetoothHandler = new Handler(){

            private void post(String key,String value, String key2, String value2)
            {
                String url="http://203.246.113.83:8080"; // URL http://xx.xxx..xx.../cardinfo.php";
                RequestBody formBody= new FormBody.Builder()
                        .add(key,value)
                        .add(key2, value2)
                        .build();
                Request request=new Request.Builder()
                        .url(url)
                        .post(formBody)
                        .build();
                client.newCall(request).enqueue(callBack);
            }
            private okhttp3.Callback callBack=new okhttp3.Callback() {
                @Override
                public void onFailure(@NotNull Call call, @NotNull IOException e) {
                    Log.d("Test","ERROR Message " +e.getMessage());
                }

                @Override
                public void onResponse(@NotNull Call call, @NotNull Response response) throws IOException {
                    if(!response.isSuccessful())
                    {
                        throw new IOException("Unexpected code " + response);
                    }
                    else
                    {
                        final String body = response.body().string(); //post이기 때문에 .string
                        Log.d("TEST", "responseData : " + body);
                        new Handler(getMainLooper()).post(new Runnable() {
                            @Override
                            public void run() {
                                JSONArray jsonArray=null;
                                Log.d("Res",body.toString());
                                try
                                {
                                    JSONObject jsonObject=new JSONObject(body);
                                    String class_name=jsonObject.getString("class");
                                    String end_class=jsonObject.getString("endclass");

                                    // char blank = '-1';
                                    // String ch_a = Character.toString(a);

                                    if(class_name.equals("-1"))
                                    {
                                        //if (click_flag){
                                        //     mimageView.setImageResource();
                                        //}

                                        Log.d("MSG","Data was sent");
                                    }
                                    else if(class_name.equals("-1"))
                                    {
                                        //if (click_flag){
                                        //     mimageView.setImageResource();
                                        //}
                                        Log.d("MSG","Data was sent");
                                    }
                                    else
                                    {
                                        if(class_name.equals("12") || class_name.equals("14") || class_name.equals("16"))
                                        {
                                            if (class_name.equals("12")){
                                                class_name = pre_class + "a";
                                            }
                                            else if (class_name.equals("14")){
                                                class_name = pre_class + "b";
                                            }
                                            else if (class_name.equals("16")){
                                                class_name = pre_class + "c";
                                            }
                                            mimageView.setImageResource(imageMap.get(class_name));
                                            second_flag = false;
                                        }
                                        else{
                                            mimageView.setImageResource(imageMap.get(class_name));
                                            second_flag = true;
                                            pre_class = class_name;
                                        }
                                        /*

                                        if(class_name.equals("-1")){
                                            mimageView.setImageResource(imageMap.get("blank"));
                                        }

                                         */
                                    }
                                } catch (JSONException e) {

                                    e.printStackTrace();
                                }


                            }
                        });
                    }
                }
            };

            public void handleMessage(android.os.Message msg){
                if(msg.what == BT_MESSAGE_READ){
                    String readMessage = null;
                    try {
                        readMessage = new String((byte[]) msg.obj, "UTF-8");
                        //Log.d("target",readMessage);

                        // flag == false
                        if(!flag) {
                            readMessage = readMessage.replace('#', '*');
                        }

                       // Log.d("Res",readMessage.toString());

                    } catch (UnsupportedEncodingException e) {
                        Log.d("exp", "critical error");
                        e.printStackTrace();
                    }

                     post("start",readMessage, "end",  String.valueOf(second_flag));// and->server

                    mTvReceiveData.setText(readMessage);
                }
            }
        };
    }


    void bluetoothOn() {
        if(mBluetoothAdapter == null) {
            Toast.makeText(getApplicationContext(), "블루투스를 지원하지 않는 기기입니다.", Toast.LENGTH_LONG).show();
        }
        else {
            if (mBluetoothAdapter.isEnabled()) {
                Toast.makeText(getApplicationContext(), "블루투스가 이미 활성화 되어 있습니다.", Toast.LENGTH_LONG).show();
                mTvBluetoothStatus.setText("활성화");



                if (mBluetoothAdapter.isEnabled()) {
                    mPairedDevices = mBluetoothAdapter.getBondedDevices();

                    if (mPairedDevices.size() > 0) {
                        AlertDialog.Builder builder = new AlertDialog.Builder(this);
                        builder.setTitle("장치 선택");

                        mListPairedDevices = new ArrayList<String>();
                        for (BluetoothDevice device : mPairedDevices) {
                            mListPairedDevices.add(device.getName());
                            //mListPairedDevices.add(device.getName() + "\n" + device.getAddress());
                        }
                        final CharSequence[] items = mListPairedDevices.toArray(new CharSequence[mListPairedDevices.size()]);
                        mListPairedDevices.toArray(new CharSequence[mListPairedDevices.size()]);

                        builder.setItems(items, new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int item) {
                                pre_device_name = pre_device_name + items[item].toString();
                                connectSelectedDevice(items[item].toString());
                            }
                        });
                        AlertDialog alert = builder.create();
                        alert.show();
                    } else {
                        Toast.makeText(getApplicationContext(), "페어링된 장치가 없습니다.", Toast.LENGTH_LONG).show();
                    }
                }
                else {
                    Toast.makeText(getApplicationContext(), "블루투스가 비활성화 되어 있습니다.", Toast.LENGTH_SHORT).show();
                }
            }
            else {
                Toast.makeText(getApplicationContext(), "블루투스가 활성화 되어 있지 않습니다.", Toast.LENGTH_LONG).show();
                Intent intentBluetoothEnable = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                startActivityForResult(intentBluetoothEnable, BT_REQUEST_ENABLE);

                while (!mBluetoothAdapter.isEnabled()){
                    SystemClock.sleep(500);
                }

                if (mBluetoothAdapter.isEnabled()) {
                    mPairedDevices = mBluetoothAdapter.getBondedDevices();

                    if (mPairedDevices.size() > 0) {
                        AlertDialog.Builder builder = new AlertDialog.Builder(this);
                        builder.setTitle("장치 선택");

                        mListPairedDevices = new ArrayList<String>();
                        for (BluetoothDevice device : mPairedDevices) {
                            mListPairedDevices.add(device.getName());
                            //mListPairedDevices.add(device.getName() + "\n" + device.getAddress());
                        }
                        final CharSequence[] items = mListPairedDevices.toArray(new CharSequence[mListPairedDevices.size()]);
                        mListPairedDevices.toArray(new CharSequence[mListPairedDevices.size()]);

                        builder.setItems(items, new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int item) {
                                pre_device_name = pre_device_name + items[item].toString();
                                connectSelectedDevice(items[item].toString());
                            }
                        });
                        AlertDialog alert = builder.create();
                        alert.show();
                    } else {
                        Toast.makeText(getApplicationContext(), "페어링된 장치가 없습니다.", Toast.LENGTH_LONG).show();
                    }
                }
            }
        }

        if(!flag) flag=true;
        //SystemClock.sleep(1000);



    }

    void bluetoothOff() {
        if (mBluetoothAdapter.isEnabled()) {
            mBluetoothAdapter.disable();
            Toast.makeText(getApplicationContext(), "이어서 인식합니다.", Toast.LENGTH_SHORT).show();
            mTvBluetoothStatus.setText("비활성화");
        }
        else {
            Toast.makeText(getApplicationContext(), "이어서 인식할 수 없습니다. REFRESH 버튼을 눌러주세요.", Toast.LENGTH_SHORT).show();
        }

        if(!flag)
        {
            flag = true;
            click_flag = false;
        }

        if(mBluetoothAdapter == null) {
            Toast.makeText(getApplicationContext(), "블루투스를 지원하지 않는 기기입니다.", Toast.LENGTH_LONG).show();
        }
        else {
            if (!mBluetoothAdapter.isEnabled()) {
                // Toast.makeText(getApplicationContext(), "블루투스가 활성화 되어 있지 않습니다.", Toast.LENGTH_LONG).show();
                Intent intentBluetoothEnable = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                startActivityForResult(intentBluetoothEnable, BT_REQUEST_ENABLE);

                while (!mBluetoothAdapter.isEnabled()){
                    SystemClock.sleep(500);
                }

                if (mBluetoothAdapter.isEnabled()) {
                    connectSelectedDevice(pre_device_name);
                    }
                else {
                        Toast.makeText(getApplicationContext(), "페어링된 장치가 없습니다.", Toast.LENGTH_LONG).show();
                    }
                }
            }
        }

        // mimageView.setImageResource(imageMap.get("-1"));


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        switch (requestCode) {
            case BT_REQUEST_ENABLE:
                if (resultCode == RESULT_OK) { // 블루투스 활성화를 확인을 클릭하였다면
                    Toast.makeText(getApplicationContext(), "블루투스 활성화", Toast.LENGTH_LONG).show();
                    mTvBluetoothStatus.setText("활성화");
                } else if (resultCode == RESULT_CANCELED) { // 블루투스 활성화를 취소를 클릭하였다면
                    Toast.makeText(getApplicationContext(), "취소", Toast.LENGTH_LONG).show();
                    mTvBluetoothStatus.setText("비활성화");
                }
                break;
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    void listPairedDevices() {
        if (mBluetoothAdapter.isEnabled()) {
            mBluetoothAdapter.disable();
            Toast.makeText(getApplicationContext(), "블루투스가 비활성화 되었습니다.", Toast.LENGTH_SHORT).show();
            mTvBluetoothStatus.setText("비활성화");
        }
        else {
            Toast.makeText(getApplicationContext(), "블루투스가 이미 비활성화 되어 있습니다.", Toast.LENGTH_SHORT).show();
        }

        if(!flag)
        {
            flag = true;
        }
        if (click_flag) click_flag = false;
        if (second_flag) second_flag = false;
        pre_device_name = "";

        mimageView.setImageResource(imageMap.get("-1"));
    }

    void connectSelectedDevice(String selectedDeviceName) {
        for(BluetoothDevice tempDevice : mPairedDevices) {
            if (selectedDeviceName.equals(tempDevice.getName())) {
                mBluetoothDevice = tempDevice;
                break;
            }
        }
        try {
            mBluetoothSocket = mBluetoothDevice.createRfcommSocketToServiceRecord(BT_UUID);
            mBluetoothSocket.connect();
            mThreadConnectedBluetooth = new ConnectedBluetoothThread(mBluetoothSocket);

            mThreadConnectedBluetooth.start();
            mBluetoothHandler.obtainMessage(BT_CONNECTING_STATUS, 1, -1).sendToTarget();
        } catch (IOException e) {
            Toast.makeText(getApplicationContext(), "블루투스 연결 중 오류가 발생했습니다.", Toast.LENGTH_LONG).show();
        }
    }

    private class ConnectedBluetoothThread extends Thread {
        private final BluetoothSocket mmSocket;
        private final InputStream mmInStream;
        private final OutputStream mmOutStream;

        public ConnectedBluetoothThread(BluetoothSocket socket) {
            mmSocket = socket;
            InputStream tmpIn = null;
            OutputStream tmpOut = null;

            try {
                tmpIn = socket.getInputStream();
                tmpOut = socket.getOutputStream();
            } catch (IOException e) {
                Toast.makeText(getApplicationContext(), "소켓 연결 중 오류가 발생했습니다.", Toast.LENGTH_LONG).show();
            }

            mmInStream = tmpIn;
            mmOutStream = tmpOut;
        }
        public void run() {

            while (true) {
                try {
                    int bytes;
                    bytes = mmInStream.available();
                    if (bytes != 0) {
                        // byte[] buffer = new byte[1024];
                        byte[] buffer = new byte[256];

                        SystemClock.sleep(500);

                        bytes = mmInStream.available();
                        bytes = mmInStream.read(buffer, 0, bytes);

                        mBluetoothHandler.obtainMessage(BT_MESSAGE_READ, bytes, -1, buffer).sendToTarget();

                        buffer=null;

                        // break;
                        //Log.d("buffer","count: "+count);
                        // buffer.finalize();
                        // buffer = null;
                    }
                } catch (IOException e) {
                    Log.d("exp","braek run");
                    break;
                }


            }
        }
        public void write(String str) {
            byte[] bytes = str.getBytes();
            try {
                mmOutStream.write(bytes);
            } catch (IOException e) {
                Toast.makeText(getApplicationContext(), "데이터 전송 중 오류가 발생했습니다.", Toast.LENGTH_LONG).show();
            }
        }
        public void cancel() {
            try {
                Log.d("Socket:","Socket is Cancle");
                mmSocket.close();
            } catch (IOException e) {
                Toast.makeText(getApplicationContext(), "소켓 해제 중 오류가 발생했습니다.", Toast.LENGTH_LONG).show();
            }
        }

    }
}