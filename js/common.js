/* shared bits */
(function(){
  // bubbles
  var b=document.createElement('div');b.className='bubbles';
  for(var i=0;i<26;i++){
    var s=document.createElement('span');
    var sz=6+Math.random()*30;
    s.style.width=sz+'px';s.style.height=sz+'px';
    s.style.left=(Math.random()*100)+'%';
    s.style.animationDuration=(9+Math.random()*16)+'s';
    s.style.animationDelay=(-Math.random()*22)+'s';
    b.appendChild(s);
  }
  document.body.appendChild(b);

  // toast
  var t=document.createElement('div');t.className='toast';document.body.appendChild(t);
  window.toast=function(msg){
    t.textContent=msg;t.classList.add('show');
    clearTimeout(t._h);t._h=setTimeout(function(){t.classList.remove('show')},2200);
  };

  // active nav
  var here=location.pathname.split('/').pop()||'index.html';
  document.querySelectorAll('.navlinks a').forEach(function(a){
    if(a.getAttribute('href')===here)a.classList.add('active');
  });
})();

window.shuffle=function(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;};
window.pick=function(a){return a[Math.floor(Math.random()*a.length)];};
