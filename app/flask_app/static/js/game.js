async function game_info()
{
    try
    {   
        const response = await fetch("/game/info", {
            method: "GET",
            credentials: "include",
        })
        const result = await response.json();
        console.log(result);
        for (let count = 0; count < result["count"].length; count++) {
            addRamp(count, result["count"][count]);
        }
        Object.keys(result.enemy_element).forEach((key, index) => {
            addTag(index, key, "ene", result.enemy_element[key], result.enemy_select);
        });

        Object.keys(result.character_element).forEach((key, index) => {
            addTag(index, key, "chr", result.character_element[key]);
        })
    }
    catch(error)
    {
        console.log(error);
    }
}

function addTag(index, id, eneorchr, element, select)
{
    // 新しい要素を作成します
    const newTag = document.createElement("div");

    // クラスを追加
    newTag.classList.add("element");
    const classMap = {
        "fire": "fire",
        "water": "water",
        "wind": "wind",
        "hidden": "back"
    };
    const cls = classMap[element];
    if (cls) {
        newTag.classList.add(cls);
    } else {
        console.log("element error");
    }
    
    let element_id = "";
    switch (eneorchr)
    {
        case "ene":
            newTag.id = "ene" + id;
            newTag.classList.add("ene");
            newTag.style.right = `calc(20vw + ${index * 10}vw)`;
            element_id = "enemy";
            break;
        case "chr":
            newTag.id = id;
            newTag.classList.add("chr");
            newTag.style.left = `calc(20vw + ${index * 10}vw)`
            element_id = "self";
            // イベントの追加
            newTag.addEventListener("click", (event) => {
                selectElement(event.currentTarget.id);
            });
            break;
        default:
            id = "battle";
    }

    // DOM に新しく作られた要素とその内容を追加します
    const currentDiv = document.getElementById(element_id);
    currentDiv.appendChild(newTag);
}

function addRamp(index, id)
{
    // console.log(index, id);
    // 新しい要素を作成します
    const newTag = document.createElement("div");

    // クラスを追加
    newTag.classList.add("ramp");
    const classMap = {
        "1": "before",
        "2": "win",
        "3": "lose",
        "4": "draw"
    };
    const cls = classMap[id];
    if (cls) {
        newTag.classList.add(cls);
    } else {
        console.log("ramp error");
    }

    // スタイルの設定
    newTag.style.top = `calc(5vh + ${index * 5}vh + ${index * 2}mm)`;

    // イベントの追加
    newTag.addEventListener("click", (event) => {
        // カードタグ設定
    });

    // DOM に新しく作られた要素とその内容を追加します
    const currentDiv = document.getElementById("gameinfo");
    currentDiv.appendChild(newTag);
}

function selectElement(id)
{
    // 既に選択されていないかチェック
    const selected = document.querySelector("#self .select");

    if (selected !== null) {
        selected.classList.remove("select");
        const choice = document.querySelector(".choice");
        choice.remove();
        if (id == selected.getAttribute("id")) {
            return
        }
    }

    element = document.getElementById(id);
    element.classList.add("select");

    // 決定ボタン表示
    const choice = document.createElement("div");
    choice.classList.add("choice");
    choice.innerHTML = "決定";
    choice.addEventListener("click", (event) => {
        game_update(id);
    });
    const currentDiv = document.getElementById("battle");
    currentDiv.appendChild(choice);
}

// ゲーム更新(更新APIから情報を基にアニメーションを差し込み、game_infoに係る情報を初期化、game_info呼び出し)
async function game_update(id)
{
    try
    {
        const response = await fetch("/game/update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({ slot: id })
        });
        const result = await response.json();
        console.log(result);
    }
    catch(error)
    {
        console.log(error);
    }
    game_clear();
    game_info();
}

function game_clear()
{
    characters = document.querySelector("#self");
    characters.innerHTML = "";
    enemys = document.querySelector("#enemy");
    enemys.innerHTML = "";
    ramps = document.querySelector("#gameinfo");
    ramps.innerHTML = "";
    choice = document.querySelector(".choice");
    choice.remove();
}