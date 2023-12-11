### Tugas 3
#### Langkah-langkah day3

1. Ketik di kolom pencarian 'composer', lalu pilih composer

![composer](ss/composer.png)

2. Jika belum enabled, pilih enable

![enable](ss/enable.png)

3. Create environment lalu pilih composer sesuai kebutuhan. Composer 1 menyediakan Airflow 1 dan 2, sedangkan Composer 2 hanya Airflow 2 namun bisa Autoscaling.
Disini saya menggunakan composer 2 sesuai demo mentor.

![composer-2](ss/composer-2.png)

4. Input nama, pilih location, image version dan pilih default service account

![fill](ss/fill.png)

Jika meminta permissions, centang kotak kecil yang disediakan lalu grant

![grant](ss/grant.png)

5. Klik create

![create](ss/create.png)

6. Tunggu hingga proses selesai

![wait](ss/wait.png)

Setelah proses selesai, environment berhasil dibuat

![created](ss/created.png)

7. Upload DAG dengan nama ```insert_data_bigquery``` yang ada pada file [insert.py](../cloud-composer/insert.py) dengan menjalankan command berikut di terminal
```
gcloud composer environments storage dags import \
    --environment my-environment \
    --location asia-southeast1 \
    --source="cloud-composer/insert.py"
```

![uploading](ss/uploading.png)

Before:
![before](ss/before.png)

After:
![uploaded](ss/uploaded.png)

8. Cek ```my_dataset.my_table``` di BigQuery

Data sudah berhasil di insert ke my_table

![inserted](ss/inserted.png)

note: DAG yang sudah berhasil diupload bisa di trigger dan di pause secara manual 

![dag](ss/dag.png)

9. Delete DAG
```
gcloud composer environments storage dags delete \
    --environment my-environment \
    --location asia-southeast1 \
    cloud-composer/insert.py
```
pilih Y

![y_delete](ss/y_delete.png)

DAG berhasil dihapus

![deleted](ss/deleted.png)
