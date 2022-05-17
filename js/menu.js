jQuery(document).ready(function(){
	if( $('.cd-stretchy-nav').length > 0 ) {
		var stretchyNavs = $('.cd-stretchy-nav');
		
		stretchyNavs.each(function(){
			var stretchyNav = $(this),
				stretchyNavTrigger = stretchyNav.find('.cd-nav-trigger');
			
			stretchyNavTrigger.on('click', function(event){
				event.preventDefault();
				stretchyNav.toggleClass('nav-is-visible');
			});
		});

		$(document).on('click', function(event){
			( !$(event.target).is('.cd-nav-trigger') && !$(event.target).is('.cd-nav-trigger span') ) && stretchyNavs.removeClass('nav-is-visible');
		});
	}
});



jQuery(document).ready(function() {

    var arrLang={
        
        'tr':{
            'meslek':
            'hedef':
            'hedef_paragraf':
            'dg':
            'numara':
            'tecrübeler':
            'tecrübe 1 başlık':
            'tecrübe 1 firma':
            'tecrübe 1 bolum':
            'tecrübe 1 p':
            'tecrübe 2 başlık':
            'tecrübe 2 firma':
            'tecrübe 2 bolum':
            'tecrübe 2 p':
            'tecrübe 3 başlık':
            'tecrübe 3 firma':
            'tecrübe 3 bolum':
            'tecrübe 3 p':
            'tecrübe 4 başlık':
            'tecrübe 4 firma':
            'tecrübe 4 bolum':
            'tecrübe 4 p':
            'tecrübe 5 başlık':
            'tecrübe 5 firma':
            'tecrübe 5 bolum':
            'tecrübe 5 p':
            'Egitim':
            'Egitim uni':
            'Egitim bolum':
            'Egitim derece':
            'Egitim lise':
        },


        'en':{
            'meslek':
            'hedef':
            'hedef_paragraf':
            'dg':
            'numara':
            'tecrübeler':
            'tecrübe 1 başlık':
            'tecrübe 1 firma':
            'tecrübe 1 bolum':
            'tecrübe 1 p':
            'tecrübe 2 başlık':
            'tecrübe 2 firma':
            'tecrübe 2 bolum':
            'tecrübe 2 p':
            'tecrübe 3 başlık':
            'tecrübe 3 firma':
            'tecrübe 3 bolum':
            'tecrübe 3 p':
            'tecrübe 4 başlık':
            'tecrübe 4 firma':
            'tecrübe 4 bolum':
            'tecrübe 4 p':
            'tecrübe 5 başlık':
            'tecrübe 5 firma':
            'tecrübe 5 bolum':
            'tecrübe 5 p':
            'Egitim':
            'Egitim uni':
            'Egitim bolum':
            'Egitim derece':
            'Egitim lise':
        },
        
        'de':{
            'meslek':
            'hedef':
            'hedef_paragraf':
            'dg':
            'numara':
            'tecrübeler':
            'tecrübe 1 başlık':
            'tecrübe 1 firma':
            'tecrübe 1 bolum':
            'tecrübe 1 p':
            'tecrübe 2 başlık':
            'tecrübe 2 firma':
            'tecrübe 2 bolum':
            'tecrübe 2 p':
            'tecrübe 3 başlık':
            'tecrübe 3 firma':
            'tecrübe 3 bolum':
            'tecrübe 3 p':
            'tecrübe 4 başlık':
            'tecrübe 4 firma':
            'tecrübe 4 bolum':
            'tecrübe 4 p':
            'tecrübe 5 başlık':
            'tecrübe 5 firma':
            'tecrübe 5 bolum':
            'tecrübe 5 p':
            'Egitim':
            'Egitim uni':
            'Egitim bolum':
            'Egitim derece':
            'Egitim lise':
        },            
    };

    
$('.dropdown-item').click(function() {
    localStorage.setItem('dil', JSON.stringify($(this).attr('id'))); 
    location.reload();
  });

    var lang =JSON.parse(localStorage.getItem('dil'));

    if(lang=="en"){
        $("#drop_yazı").html("English");
    }
    if(lang=="tr"){
        $("#drop_yazı").html("Türkçe");
    }
    if(lang=="de"){
        $("#drop_yazı").html("Deutsch");
    }        
    
    $('a,h5,p,h1,h2,span,li,button,h3,label').each(function(index,element) {
      $(this).text(arrLang[lang][$(this).attr('key')]);
    
  });

});