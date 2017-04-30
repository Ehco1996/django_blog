function playPause() {
    var music = document.getElementById('music2');
    var music_btn = document.getElementById('music_btn2');
    if (music.paused) {
        music.play();

    }
    else {
        music.pause();

    }
}

/* Display table of contents */
function show_toc(toc_selector, wrap_id, min_nr)
{
    var wrap = document.getElementById(wrap_id);

    var hlist = document.querySelectorAll(toc_selector);

    if (!wrap)
        return;
     
    if (!hlist || hlist.length <= min_nr) {
        wrap.style.display = 'none';
        return;
    }
   
    

    var ul = document.createElement('ul'), li, link;
    
    for (i = 0; i < hlist.length; i++) {
        hlist[i].id = 'i_' + i;

        li = document.createElement('li');

        link = document.createElement('a');
        link.href = '#' + hlist[i].id;
        link.className = 'toc_link';
        link.innerHTML = hlist[i].innerHTML;
        
        li.appendChild(link);
        ul.appendChild(li);
    }

    wrap.appendChild(ul);
}