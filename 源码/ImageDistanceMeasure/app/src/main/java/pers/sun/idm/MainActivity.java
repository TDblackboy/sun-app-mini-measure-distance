package pers.sun.idm;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import pers.sun.R;

public class MainActivity extends AppCompatActivity {

    //申请相机权限的码
    public static final int PERMISSION_CEMERA_REQUEST_CODE = 0x00000012;//声明一个请求码，用于识别返回的结果

    //用于保存照片的uri
    private Uri mCameraUri;

    //照片的保存路径
    private String mCameraPicPath;

    //是否是android10以上的手机
    private final boolean isAndroidQ = Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q;

    //绑定UI组件 image view
    private ImageView imageView;

    //后端地址
    private String ip = "192.168.43.138";
    private int port = 8001;
    //private String remoteUrl = "http://" + ip + ":" + port + "/maybe/md";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //加载布局
        setContentView(R.layout.activity_main);

        //imageView绑定ImageView组件
        imageView = (ImageView) findViewById(R.id.imageView);

    }

    /**
     * 点击处理过程：点击->进入拍照功能：返回一张图片->上传服务器->接受服务器响应：根据响应返回信息
     *
     * @param view
     */
    public void btnClick(View view) {
        //拍照，设置uri
        if (checkPermissionAndCamera()) {
            openCamera();
        } else {
            ActivityCompat.requestPermissions(
                    this,
                    new String[]{
                            Manifest.permission.CAMERA,
                            Manifest.permission.WRITE_EXTERNAL_STORAGE,
                            Manifest.permission.READ_EXTERNAL_STORAGE},
                    PERMISSION_CEMERA_REQUEST_CODE);
        }

    }


    //检查相机权限
    private boolean checkPermissionAndCamera() {
        System.out.println(">>> 检查是否有拍照权限");
        int hasPermission = ContextCompat.checkSelfPermission(getApplication(), Manifest.permission.CAMERA);

        if (hasPermission == PackageManager.PERMISSION_GRANTED) {
            System.out.println("有拍照权限");
            //openCamera();
            return true;
        } else {
            System.out.println("没有拍照权限");
            //ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, PERMISSION_CEMERA_REQUEST_CODE);
            /*ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.READ_EXTERNAL_STORAGE},
                    PERMISSION_CEMERA_REQUEST_CODE);*/
            return false;
        }
    }

    //授权回调
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        System.out.println(">>> 授权结果");
        System.out.println(requestCode);
        System.out.println(PERMISSION_CEMERA_REQUEST_CODE);
        if (requestCode == PERMISSION_CEMERA_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                openCamera();
            } else {
                Toast.makeText(this, "拍照未授权", Toast.LENGTH_SHORT).show();
            }
        }
    }

    //调用拍照功能
    private void openCamera() {
        System.out.println(">>> 开启拍照");
        Intent captureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        //判断是否有相机
        if (captureIntent.resolveActivity(getPackageManager()) != null) {
            System.out.println("有相机");
            File photoFile = null;
            Uri photoUri = null;
            if (isAndroidQ) {
                //android10及以上？的处理方式
                System.out.println("android版本>=10:" + isAndroidQ);
                photoUri = createPhotoUri();
            } else {
                System.out.println("android版本< 10");
                //photoFile=createPhotoFile();
                /*if(photoFile!=null){
                }*/
            }

            mCameraUri = photoUri;
            System.out.println("mCameraUri is :" + mCameraUri);
            if (photoUri != null) {
                captureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoUri);
                captureIntent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
                startActivityForResult(captureIntent, PERMISSION_CEMERA_REQUEST_CODE);
            }
        } else {
            System.out.println("没有相机");
        }

    }

    //拍照后的uri
    private Uri createPhotoUri() {
        System.out.println(">>> 照片uri");
        String status = Environment.getExternalStorageState();
        System.out.println("status:" + status);

        if (status.equals(Environment.MEDIA_MOUNTED)) {
            return getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, new ContentValues());
        } else {
            return getContentResolver().insert(MediaStore.Images.Media.INTERNAL_CONTENT_URI, new ContentValues());
        }
    }

    //接受结果，显示结果
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        System.out.println(">>> 显示照片");
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == PERMISSION_CEMERA_REQUEST_CODE) {
            if (resultCode == RESULT_OK) {
                if (isAndroidQ) {
                    System.out.println("设置image view内容");
                    //imageView.setImageURI(mCameraUri);

                    try {
                        System.out.println("从uri读取数据");
                        byte[] bytes = readImageFromUri();
                        System.out.println("请求后端处理");
                        String remoteUrl = "http://" + ip + ":" + port + "/maybe/md";
                        sendHttpRequest(remoteUrl, bytes);

                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                } else {
                    //使用图片路径加载 setImageBitMap
                    imageView.setImageBitmap(BitmapFactory.decodeFile(mCameraPicPath));
                }
            } else {
                Toast.makeText(this, "取消", Toast.LENGTH_SHORT).show();
            }
        }
    }

    //从uri中读取图片的二进制数据返回
    private byte[] readImageFromUri() throws IOException {
        String path = getPathFromUri();
        File file = new File(path);
        //InputStream inputStream=new FileInputStream(file);
        DataInputStream dataInputStream = new DataInputStream(new FileInputStream(path));
        //创建一个字节数组  byte的长度等于二进制图片的返回的实际字节数
        byte[] b = new byte[dataInputStream.available()];
        //读取图片信息放入这个b数组
        dataInputStream.read(b);
        return b;
    }

    private String getPathFromUri() {
        String realPath = getRealPathApi19Above();
        System.out.println("image path:" + realPath);
        // /storage/emulated/0/Pictures/1641721564231.jpg
        //File file = new File(img_path);
        return realPath;
    }

    private String getRealPathApi19Above() {
        String filePath = "";
        Uri uri = mCameraUri;
        try {
            final boolean isKitKat = Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT;

            // DocumentProvider
            if (isKitKat && DocumentsContract.isDocumentUri(this, uri)) {
                // MediaProvider
                if (isMediaDocument(uri)) {
                    final String docId = DocumentsContract.getDocumentId(uri);
                    final String[] split = docId.split(":");
                    final String type = split[0];

                    Uri contentUri = null;
                    if ("image".equals(type)) {
                        contentUri = MediaStore.Images.Media.EXTERNAL_CONTENT_URI;
                    } else if ("video".equals(type)) {
                        contentUri = MediaStore.Video.Media.EXTERNAL_CONTENT_URI;
                    } else if ("audio".equals(type)) {
                        contentUri = MediaStore.Audio.Media.EXTERNAL_CONTENT_URI;
                    }

                    final String selection = "_id=?";
                    final String[] selectionArgs = new String[]{
                            split[1]
                    };

                    return getDataColumn(this, contentUri, selection, selectionArgs);
                }
            }
            // MediaStore (and general)
            else if ("content".equalsIgnoreCase(uri.getScheme())) {

                // Return the remote address
                if (isGooglePhotosUri(uri))
                    return uri.getLastPathSegment();

                return getDataColumn(this, uri, null, null);
            }
            // File
            else if ("file".equalsIgnoreCase(uri.getScheme())) {
                return uri.getPath();
            }

        } catch (Exception e) {
            filePath = "";
        }
        return filePath;
    }

    public static boolean isMediaDocument(Uri uri) {
        return "com.android.providers.media.documents".equals(uri.getAuthority());
    }

    public static boolean isGooglePhotosUri(Uri uri) {
        return "com.google.android.apps.photos.content".equals(uri.getAuthority());
    }

    public static String getDataColumn(Context context, Uri uri, String selection, String[] selectionArgs) {
        Cursor cursor = null;
        final String column = "_data";
        final String[] projection = {
                column
        };

        try {
            cursor = context.getContentResolver().query(uri, projection, selection, selectionArgs,
                    null);
            if (cursor != null && cursor.moveToFirst()) {
                final int index = cursor.getColumnIndexOrThrow(column);
                return cursor.getString(index);
            }
        } finally {
            if (cursor != null)
                cursor.close();
        }
        return null;
    }

    //发起http请求
    //创建新线程
    private void sendHttpRequest(String remoteUrl, byte[] input) throws IOException {
        //发送的信息
        //String remoteUrl = "http://" + ip + ":" + port + "/maybe/md";
        //String remoteUrl = "http://127.0.0.1:8001/maybe/md";
        MediaType MEDIA_TYPE_TEXT = MediaType.parse("image/jpg");
        //开启子线程
        new Thread(new Runnable() {
            @Override
            public void run() {
                //
                OkHttpClient client = new OkHttpClient();

                //构建一个请求
                RequestBody body = RequestBody.Companion.create(input, MEDIA_TYPE_TEXT);

                Request request = new Request.Builder()
                        .url(remoteUrl)
                        .post(body)
                        .build();

                //send and receive
                try (Response response = client.newCall(request).execute()) {
                    //后端返回的响应是图片-字节
                    System.out.println("响应结果：");
                    final byte[] res = response.body().bytes();
                    System.out.println(res);
                    handlerReponse(res);
                    //imageView = (ImageView) findViewById(R.id.imageView);
                    //imageView.setImageBitmap(getBitmapFromByte(response.body().bytes()));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();


    }

    private void handlerReponse(final byte[] res) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                //这里进行UI操作
                System.out.println("显示响应的图片");
                imageView.setImageBitmap(getBitmapFromByte(res));
            }
        });
    }

    public Bitmap getBitmapFromByte(byte[] temp) {
        if (temp != null) {
            Bitmap bitmap = BitmapFactory.decodeByteArray(temp, 0, temp.length);
            return bitmap;
        } else {
            return null;
        }
    }


}