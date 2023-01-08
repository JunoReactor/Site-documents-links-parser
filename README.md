# Site-documents-links-parser

Парсит страницы сайта и вытаскивает оттуда все ссылки на документы, их заголовки описаны в массиве:<br>

```headers = ["application/force-download","application/x-compress","application/x-gzip","application/x-zip","application/zip","application/x-tiff","application/tiff","application/compact_pro","application/tif","application/x-tif","image/tif","image/x-tif","image/x-tiff","application/pdf","application/msword","application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/vnd.openxmlformats-officedocument.wordprocessingml.template","application/vnd.ms-word.document.macroEnabled.12","application/vnd.ms-word.template.macroEnabled.12","image/jpeg","video/mp4","image/png","application/vnd.openxmlformats-officedocument.presentationml.presentation","application/vnd.ms-excel","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet","application/zip","image/jpg","application/x-7z-compressed","application/vnd.rar","application/x-rar-compressed","application/octet-stream","application/zip, application/octet-stream", "application/x-zip-compressed", "multipart/x-zip","application/rtf","application/vnd.ms-powerpoint","video/mp4","audio/mpeg","image/gif","application/gzip","text/csv","audio/aac"]```<br><br>

## Как с этим работать:<br><br>
```sh
python3 li.py URL -m [количество итераций int] -s [количество сек. ожидания float]
python3 li.py http://site.com/ -m 0  -s 0.3
python3 li.py http://site.com/ --max-urls 0  --sleep 0.3
```
<br><br>
## По итогу создается текстовых файла:<br>
| LOG файл | Описание |
| ------ | ------ |
| [site-name]_internal_link.txt | ссылки страницы что удалось обойти |
| [site-name]_internal_file_link.txt | ссылки на файлы |

