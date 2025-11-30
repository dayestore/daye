// السلايدر تلقائي - لا يحتاج تدخل المستخدم
// الكود بسيط فقط لتأكيد التشغيل بدون مشاكل
console.log("Daye slider running smoothly 🌸");

// Force small social icon size (fallback)
document.addEventListener('DOMContentLoaded', function() {
  var icons = document.querySelectorAll('.social-icons img, .social-icons svg, .social-icons image');
  icons.forEach(function(el){
    el.style.width = '18px';
    el.style.height = '18px';
    el.style.maxWidth = '18px';
    el.style.maxHeight = '18px';
    el.style.objectFit = 'contain';
    el.style.display = 'block';
    // إذا كانت صورة كبيرة جداً داخل الملف، ننقص أبعاد الـ parent لنتأكد
    var p = el.closest('a');
    if (p) {
      p.style.width = '34px';
      p.style.height = '34px';
      p.style.minWidth = '34px';
      p.style.minHeight = '34px';
      p.style.padding = '4px';
    }
  });
});

