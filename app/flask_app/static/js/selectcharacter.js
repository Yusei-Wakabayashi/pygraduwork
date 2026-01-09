async function addcharacter()
{
    try
    {
        const response = await fetch("/character/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({ value: "" })
        });
        console.log(response);
    }
    catch(error)
    {
        console.log(error);
    }
}

async function characterlist()
{
    try{   
        const response = await fetch("/character/list", {
            method: "GET",
            credentials: "include"
        })
        const result = await response.json();
        console.log(result);
        result.forEach((item, index) => {
            addImg(index, item.id, item.image);
        });
    }
    catch(error)
    {

    }
}

function addImg(index, id, image_path)
{
    // 新しいimg要素を作成します
    const newImg = document.createElement("img");

    // 画像パスを指定します
    newImg.src = image_path;

    // idを指定
    newImg.id = id;

    // クラスを追加
    newImg.classList.add("character");
    newImg.classList.add("position");

    // スタイルの設定
    newImg.style.left = `${index * 40}vh`;

    // イベントの追加
    newImg.addEventListener("click", (event) => {
        gameinit(event.currentTarget.id);
    });

    // DOM に新しく作られた要素とその内容を追加します
    const currentDiv = document.getElementById("characterlist");
    currentDiv.appendChild(newImg);
}

async function gameinit(id)
{
    try
    {
        const response = await fetch("/game/init", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({ character_id: id })
        });
        const result = await response.json();
        console.log(result);
        // // cookieにゲームid保存
        // document.cookie = 'game_id=' + result;
        window.location.href = "/game";
    }
    catch(error)
    {
        console.log(error);
    }
}
