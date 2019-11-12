
function check(all){
    var categories = JSON.parse(all)
    var name = document.getElementById('newcat').value
    var ret = false
    for (var i = 0; i < categories.length; i++) {
        console.log(categories[i])
        if (name == categories[i]) ret = true;
    }
    if (ret) alert('Категория уже существует')
    else document.forms['myform'].submit()
}

function close_w() {
    window.close();
}

function set_sort(num, filter, cpp){
    var t, sm = new URL(document.location).searchParams.get('sortMethod')
    switch (num){
        case 1: {
            t = "?filter="+filter+"&sortMethod=1&page=1&cpp="+cpp
            if (sm == '1')  t = "?filter="+filter+"&sortMethod=1R&page=1&cpp="+cpp
            if (sm == '1R') t = "?filter="+filter+"&sortMethod=1&page=1&cpp="+cpp
        } break
        case 2: {
            t = "?filter="+filter+"&sortMethod=2&page=1&cpp="+cpp
            if (sm == '2')  t = "?filter="+filter+"&sortMethod=2R&page=1&cpp="+cpp
            if (sm == '2R') t = "?filter="+filter+"&sortMethod=2&page=1&cpp="+cpp 
        } break
        case 3: {
            t = "?filter="+filter+"&sortMethod=3&page=1&cpp="+cpp
            if (sm == '3')  t = "?filter="+filter+"&sortMethod=3R&page=1&cpp="+cpp
            if (sm == '3R') t ="?filter="+filter+"&sortMethod=3&page=1&cpp="+cpp 
        } break
    }
    window.location.href = t
}

function add(){
    window.open('newedit','Добавить товар', 'width=800,height=500,top=200,left=400');
    return false;
}

function edit(goodpk){
    window.open('newedit?edit='+goodpk,'Редактировать товар', 'width=800,height=500,top=200,left=400');
    return false;
}

function confirmDelete(target, pagenum, cpp){
    if (confirm('Это действие удалит все товары этой категории. Вы уверены?\n'+target)) window.location.href = '?page='+pagenum+'&cpp'+cpp+'&delete='+target
}

function delete_g(name, target, pagenum, sortMethod, filter, cpp){
    if (confirm('Это действие удалит следующий товар. Вы уверены?\n'+name)) window.location.href = '?filter='+filter+'&sortMethod'+sortMethod+'&page='+pagenum+'&cpp'+cpp+'&delete='+target
}


function selectcat(){
    var cat = document.getElementById('catselect').value
    window.location.href='?filter='+cat
};

function select(target, pagenum, sortMethod, filter){
    var c = (target) ? document.getElementById("selector_d").value : document.getElementById("selector_u").value
    window.location.href='?page='+pagenum+'&filter='+filter+'&sortMethod='+sortMethod+'&cpp='+c
}

function select_good_cat(){
    var c = document.getElementById("catselector").value
    console.log(c)
    document.getElementById("cat").value = c
}