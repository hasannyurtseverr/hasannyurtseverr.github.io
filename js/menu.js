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

            '0':'Chania',
            'hasan':'Uçuş',
            '2':'Şehir',
            '3':'Ada',
            '4':'Yemek',
            '5':'Şehir',
            '6':'Hanya, Girit adasındaki Hanya bölgesinin başkentidir. Şehir iki kısma ayrılabilir, eski şehir ve modern şehir',
            '7':'Ne?',
            '8':'Hanya, Girit adasında bir şehirdir.',
            '9':'Nerede ?',
            '10':'Girit Mediterranea denizinde bir yunan adasıdır ',
            '11':"Nasıl?",
            '12':"Avrupa'nın her yerinden Hanya havalimanına ulaşabilirsiniz.",
            '13':'İçeriğin yeniden boyutlandırmaya nasıl yanıt verdiğini görmek için tarayıcı penceresini yeniden boyutlandırın.'
 


        },


        'en':{
            '0':'Chania',
            'hasan':'The Flight',
            '2':'The City',
            '3':'The Island',
            '4':'The Food',
            '5':'The City',
            '6':'Chania is the capital of the Chania region on the island of Crete. The city can be divided in two parts, the old town and the modern city.',
            '7':'What?',
            '8':'Chania is a city on the island of Crete.',
            '9':'Where?',
            '10':'Crete is a Greek island in the Mediterranean Sea.',
            '11':'How?',
            '12':'You can reach Chania airport from all over Europe.',
            '13':'Resize the browser window to see how the content respond to the resizing.'
        },
        
        'de':{
            '0':'Alm',
            'hasan':'Was machst du?',
            '2':'The City',
            '3':'The Island',
            '4':'The Food',
            '5':'The City',
            '6':'Chania is the capital of the Chania region on the island of Crete. The city can be divided in two parts, the old town and the modern city.',
            '7':'What?',
            '8':'Chania is a city on the island of Crete.',
            '9':'Where?',
            '10':'Crete is a Greek island in the Mediterranean Sea.',
            '11':'How?',
            '12':'You can reach Chania airport from all over Europe.',
            '13':'Resize the browser window to see how the content respond to the resizing.'
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