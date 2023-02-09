function getDeviceLanguage(){
    cookie= document.cookie
    if (cookie.includes("lang=") == false){
        var language = navigator.language;
        if (language == "tr-TR") {
            var langcookie = "tr";
            
        }else{
            var langcookie= "en";
        }
        document.cookie = document.cookie + "lang="+langcookie+";"
        console.log(language)
        window.location.assign('/')
    }
    
}