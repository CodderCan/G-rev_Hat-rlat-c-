# Yapılacaklar Listesi (Task Reminder)

Bu program, kullanıcıların görevlerini zamanlayarak hatırlatmalar almasını sağlayan basit bir masaüstü uygulamasıdır. Kullanıcılar görevleri ekler, her görev için belirli bir tarih ve saat belirtir ve zaman geldiğinde, program kullanıcıyı hatırlatır. Uygulama, Python'un `tkinter` kütüphanesini ve çoklu iş parçacığı (multithreading) kullanarak arka planda görevleri kontrol eder.

## Özellikler

- **Görev Ekleme**: Kullanıcılar görevlerini açıklama ve zaman bilgisiyle eklerler.
- **Hatırlatmalar**: Görevlerin zamanına göre otomatik olarak bildirimler gösterilir.
- **JSON Depolama**: Görevler, bir JSON dosyasında saklanır ve program yeniden başlatıldığında kaybolmaz.
- **Çoklu İş Parçacığı**: Arka planda çalışan bir iş parçacığı ile hatırlatmalar periyodik olarak kontrol edilir.
- **Kullanıcı Dostu Arayüz**: Basit ve anlaşılır bir Tkinter arayüzü ile görevler eklenip görüntülenebilir.

## Gereksinimler

Bu uygulamanın çalışabilmesi için aşağıdaki kütüphaneler gereklidir:

- Python 3.x
- `tkinter` (Python ile birlikte gelir)
- `plyer` (Sistem bildirimleri için)

Aşağıdaki komutları kullanarak gerekli kütüphaneyi yükleyebilirsiniz:

```bash
pip install plyer
