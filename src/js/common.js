/* shared bits */

/* Safe storage: sandboxed previews (iframe without allow-same-origin) throw a
   SecurityError on any localStorage access, which would kill the whole script. */
window.store = (function(){
  var mem = {}, ok = false;
  try { var k='__t'; window.localStorage.setItem(k,'1'); window.localStorage.removeItem(k); ok = true; } catch(e){ ok = false; }
  return {
    available: ok,
    get: function(k){ try { return ok ? window.localStorage.getItem(k) : (k in mem ? mem[k] : null); } catch(e){ return (k in mem ? mem[k] : null); } },
    set: function(k,v){ v = String(v); mem[k] = v; try { if(ok) window.localStorage.setItem(k,v); } catch(e){} }
  };
})();

window.shuffle=function(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;};
window.pick=function(a){return a[Math.floor(Math.random()*a.length)];};

(function(){
  // bubbles (fewer on small screens / none if the device prefers reduced motion)
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!reduce){
    var n = window.innerWidth < 700 ? 12 : 26;
    var b=document.createElement('div');b.className='bubbles';
    for(var i=0;i<n;i++){
      var s=document.createElement('span');
      var sz=6+Math.random()*28;
      s.style.width=sz+'px';s.style.height=sz+'px';
      s.style.left=(Math.random()*100)+'%';
      s.style.animationDuration=(9+Math.random()*16)+'s';
      s.style.animationDelay=(-Math.random()*22)+'s';
      b.appendChild(s);
    }
    document.body.appendChild(b);
  }

  // toast
  var t=document.createElement('div');t.className='toast';document.body.appendChild(t);
  window.toast=function(msg){
    t.textContent=msg;t.classList.add('show');
    clearTimeout(t._h);t._h=setTimeout(function(){t.classList.remove('show')},2400);
  };

  // hamburger
  var tog=document.querySelector('.navtoggle'), links=document.querySelector('.navlinks');
  if(tog&&links){
    tog.addEventListener('click',function(){
      var open=links.classList.toggle('open');
      tog.setAttribute('aria-expanded', open?'true':'false');
    });
    links.addEventListener('click',function(e){
      if(e.target.tagName==='A'){links.classList.remove('open');tog.setAttribute('aria-expanded','false');}
    });
  }

  // active nav
  var here=location.pathname.split('/').pop()||'index.html';
  document.querySelectorAll('.navlinks a').forEach(function(a){
    if(a.getAttribute('href')===here)a.classList.add('active');
  });
})();
