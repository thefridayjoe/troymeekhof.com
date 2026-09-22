(function(){
  if(!document.getElementById('modeLabel'))return;
  var copy={
    all:{label:"Caledonia, Michigan",h1:"Filmmaker. Marketer.<br><span>The Cybertruck Guy.</span>",lede:"I'm Troy Meekhof — a West Michigan filmmaker and digital marketer who's filmed dozens and dozens of weddings, 10x'd a mortgage lender's traffic, and built a 50-million-view audience around one very shiny truck."},
    weddings:{label:"Mid-July Media",h1:"No wedding should be<br><span>left unfilmed.</span>",lede:"Michigan wedding films since 2019. Highlights and full documentaries, drone included, no travel fee in the Lower Peninsula — and I'm the videographer at every single one."},
    marketing:{label:"Grand Rapids Marketing Co.",h1:"Brilliant marketing<br><span>for any budget.</span>",lede:"SEO, GEO, video, and websites for small businesses. I took a mortgage lender from 50 to 500 clicks a day; start with a free Search Gap Audit for yours."},
    cybertruck:{label:"@cybrtrkguy",h1:"The Cybertruck<br><span>Guy.</span>",lede:"Owner since 2024. 50M impressions a year of honest ownership content: range tests, mods, road trips, and the $1,000-off Tesla referral link. Quoted in Newsweek."},
    adventure:{label:"Serial road-tripper",h1:"Michigan to Montana,<br><span>and back.</span>",lede:"Overlanding, camping, dunes, and drone footage from 4,500-mile road trips — in a stainless steel truck that shouldn't work as an adventure rig, but does."},
    local:{label:"Village of Caledonia",h1:"West Michigan,<br><span>born and stayed.</span>",lede:"Restoring a 1915 stucco house, raising a kid, GVSU class of 2020, Tesla Owners Club of Michigan, and always chasing the next cheap breakfast joint."}
  };
  var root=document.documentElement,btns=document.querySelectorAll('.modes a[data-set]');
  function setMode(m){
    if(!copy[m])m='all';
    root.setAttribute('data-mode',m);
    btns.forEach(function(b){if(b.dataset.set===m){b.setAttribute('aria-current','page')}else{b.removeAttribute('aria-current')}});
    document.getElementById('modeLabel').textContent=copy[m].label;
    document.getElementById('h1').innerHTML=copy[m].h1;
    document.getElementById('lede').textContent=copy[m].lede;
    document.querySelectorAll('[data-m]').forEach(function(el){el.hidden=(m!=='all'&&el.dataset.m.split(' ').indexOf(m)<0)});
    try{localStorage.setItem('tm-mode',m)}catch(e){}
    if(location.hash.replace('#','')!==m&&m!=='all')history.replaceState(null,'','#'+m);
    if(m==='all'&&location.hash)history.replaceState(null,'',location.pathname);
  }
  // On the home page the mode pills filter in place; the hrefs stay as real links for crawlers and new tabs.
  btns.forEach(function(b){b.addEventListener('click',function(e){if(e.metaKey||e.ctrlKey||e.shiftKey||e.button!==0)return;e.preventDefault();setMode(b.dataset.set);})});
  var h=location.hash.replace('#','');
  setMode(copy[h]?h:'all');
  window.addEventListener('hashchange',function(){var x=location.hash.replace('#','');setMode(copy[x]?x:'all')});
})();
