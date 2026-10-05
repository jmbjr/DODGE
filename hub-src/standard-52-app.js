const pipStyles=document.createElement("link");pipStyles.rel="stylesheet";pipStyles.href="../../../../hub-pips.css";document.head.append(pipStyles);
const model = await fetch("./resolved.json").then(response => {
  if (!response.ok) throw new Error(`resolved model: ${response.status}`);
  return response.json();
});
const declared = model.cards.map(card => ({ ...card }));
let deck = declared.map(card => ({ ...card }));
let drawn = null;
let discard = [];
const $ = id => document.getElementById(id);
const layouts = {
  2:[[50,72,0],[50,28,180]], 3:[[50,74,0],[50,50,0],[50,26,180]],
  4:[[30,72,0],[70,72,0],[30,28,180],[70,28,180]],
  5:[[30,72,0],[70,72,0],[50,50,0],[30,28,180],[70,28,180]],
  6:[[30,74,0],[70,74,0],[30,50,0],[70,50,0],[30,26,180],[70,26,180]],
  7:[[30,76,0],[70,76,0],[50,63,0],[30,50,0],[70,50,0],[30,24,180],[70,24,180]],
  8:[[30,76,0],[70,76,0],[50,63,0],[30,50,0],[70,50,0],[50,37,180],[30,24,180],[70,24,180]],
  9:[[30,78,0],[70,78,0],[30,60,0],[70,60,0],[50,50,0],[30,40,180],[70,40,180],[30,22,180],[70,22,180]],
  10:[[30,79,0],[70,79,0],[50,69,0],[30,59,0],[70,59,0],[30,41,180],[70,41,180],[50,31,180],[30,21,180],[70,21,180]],
};
function center(card) {
  if (card.rank_order === 1) return `<strong class="ace">${card.suit_symbol}</strong>`;
  if (card.rank_order <= 10) {
    const pips = layouts[card.rank_order].map(([x,y,rotation]) => `<i style="left:${x}%;top:${100-y}%;transform:translate(-50%,-50%) rotate(${rotation}deg)">${card.suit_symbol}</i>`).join("");
    return `<span class="pips">${pips}</span>`;
  }
  return `<span class="court"><b>${card.rank_label}</b><i>${card.suit_symbol}</i></span>`;
}
function cardElement(card, small=false) {
  const element=document.createElement("article");element.className=`playing-card ${card.color} ${small?"small":""}`;
  element.innerHTML=`<span class="corner">${card.rank_label}<br>${card.suit_symbol}</span>${center(card)}<span class="corner bottom">${card.rank_label}<br>${card.suit_symbol}</span>`;element.title=card.name;return element;
}
function render() {
  $("deckCount").textContent=`(${deck.length})`;$("discardCount").textContent=`(${discard.length})`;$("deck").innerHTML=deck.length?'<div class="card-back">DODGE</div>':'<p>Empty</p>';
  $("drawn").replaceChildren(...(drawn?[cardElement(drawn)]:[]));$("discard").replaceChildren(...(discard.length?[cardElement(discard.at(-1))]:[]));$("draw").disabled=!deck.length||!!drawn;$("discardButton").disabled=!drawn;
}
function shuffle(){for(let index=deck.length-1;index>0;index--){const other=Math.floor(Math.random()*(index+1));[deck[index],deck[other]]=[deck[other],deck[index]]}render()}
$("shuffle").onclick=shuffle;$("draw").onclick=()=>{drawn=deck.shift()||null;render()};$("discardButton").onclick=()=>{if(drawn)discard.push(drawn);drawn=null;render()};$("reset").onclick=()=>{deck=declared.map(card=>({...card}));drawn=null;discard=[];render()};
$("identity").innerHTML=`<span>DODGE <code>${model.dodge_version}</code></span><span>Document <code>${model.document_id}</code></span><span>Source <code>${model.document_sha256.slice(0,12)}</code></span><span>Catalog <code>${model.catalog.sha256.slice(0,12)}</code></span>`;for(const card of declared)$("inventory").append(cardElement(card,true));render();
