import csv

def delete_row_by_sno(csv_file, sno, output_file):
    # 儲存刪除特定"sno"的列後的結果
    updated_rows = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        
        for row in reader:
            if row['sno'] != sno:
                updated_rows.append(row)

    # 寫入更新後的資料到新的 CSV 檔案
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"The row with sno {sno} has been deleted. The updated data is saved in {output_file}.")

# 使用範例
csv_file = 'NN_project/data_test.csv'           # 替換成你的 CSV 檔案路徑
sno_to_delete = '500113069'           # 替換成你要刪除的"sno"
output_file = 'NN_project/updated_data_test.csv'  # 替換成你想要儲存更新資料的檔案路徑

delete_row_by_sno(csv_file, sno_to_delete, output_file)
