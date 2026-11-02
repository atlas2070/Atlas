/* ================= Compte : connexion réservée aux membres inscrits (Supabase) =================
   Intégré dans dist/index.html par build.py (marqueur __COMPTE__), après le script principal.
   - Connexion : la personne saisit son e-mail ; si l'adresse est dans la table « members » (can_join),
     Supabase lui envoie un code (6 à 10 chiffres) à saisir ici. Pas de mot de passe.
   - Le code du site est public : ce contrôle réserve le site aux membres, il ne cache pas les données.
     Les vraies protections sont les règles RLS de supabase/setup.sql.
   Ne jamais écrire de balise fermante « script » dans ce fichier : il est inséré dans une balise script. */
const SB_URL=CONFIG.SUPABASE_URL,SB_KEY=CONFIG.SUPABASE_ANON_KEY; // réglages dans src/config.js
const OFF_DAYS=Math.max(1,+CONFIG.OFFLINE_DAYS||30);
const ACC_KEY='atlas-acces',PEND_KEY='atlas-code';
let AUTH={ok:false,email:'',role:'',uid:'',offline:false};
let sb=null;
const lsGet=k=>{try{return JSON.parse(localStorage.getItem(k)||'null')}catch(e){return null}};
const lsSet=(k,v)=>{try{v==null?localStorage.removeItem(k):localStorage.setItem(k,JSON.stringify(v))}catch(e){}};
const ssGet=k=>{try{return JSON.parse(sessionStorage.getItem(k)||'null')}catch(e){return null}};
const ssSet=(k,v)=>{try{v==null?sessionStorage.removeItem(k):sessionStorage.setItem(k,JSON.stringify(v))}catch(e){}};
const accessOK=(c,email)=>!!(c&&c.email&&c.uid&&(!email||c.email===email)&&Date.now()-c.at<OFF_DAYS*DAY);
const isNetErr=e=>!!e&&(e.status===0||e.status>=500||e.name==='AuthRetryableFetchError'||/fetch|network|load failed|internet/i.test(String(e.message||e)));
const normEmail=s=>String(s||'').trim().toLowerCase();
const EMAIL_RE=/^[^\s@,;<>()"']+@[^\s@,;<>()"']+\.[a-z]{2,}$/i;
const isAdmin=()=>AUTH.ok&&AUTH.role==='admin';
const MSG_NOT_MEMBER="Cette adresse n'est pas dans la liste des membres.";
const ORG=String(CONFIG.ORG_NAME||'').trim();
const CONTACT=()=>"l'équipe Atlas"+(CONFIG.CONTACT_EMAIL?' ('+CONFIG.CONTACT_EMAIL+')':'');

/* ---------- écran verrouillé ---------- */
function lockUI(){AUTH.ok=false;document.body.classList.add('locked');document.querySelectorAll('.sheet-bg').forEach(m=>m.remove());run=null}
function authScreen(html){lockUI();const v=$('#view');
  v.innerHTML=`<div class="auth"><div class="abrand"><span class="mark" aria-hidden="true">A</span><div><b>Atlas</b><small>Annales corrigées du S1${ORG?' · '+esc(ORG):''}</small></div></div>${html}</div>`;
  scrollTo(0,0);return v.querySelector('.auth')}
function showMsg(box,msg,kind){let p=box.querySelector('.amsg.live');
  if(!p){p=document.createElement('p');p.setAttribute('role','alert');box.querySelector('.panel').prepend(p)}
  p.className='amsg live'+(kind?' '+kind:'');p.textContent=msg}

/* ---------- démarrage ---------- */
async function bootCompte(){
  const cache=lsGet(ACC_KEY);
  if(!window.supabase||!window.supabase.createClient){ // bibliothèque de connexion non chargée (hors ligne ?)
    if(accessOK(cache))return grant(cache,true);
    return screenOffline()}
  makeClient();
  let session=null,err=null;
  try{const r=await sb.auth.getSession();session=r.data&&r.data.session;err=r.error}catch(e){err=e}
  if(session&&session.user&&session.user.email)return afterLogin(session.user);
  if(accessOK(cache)&&(!navigator.onLine||(err&&isNetErr(err))))return grant(cache,true);
  screenLogin({});
}
const SB_LIB='https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js'; // même adresse que dans app_template.html
function makeClient(){sb=window.supabase.createClient(SB_URL,SB_KEY,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true,flowType:'implicit',storageKey:'atlas-auth'},global:{fetch:sbFetch}})}
let libLoading=null;
function ensureSb(){ // bibliothèque absente au chargement (hors ligne) : on la recharge au retour du réseau
  if(sb)return Promise.resolve(true);
  if(window.supabase&&window.supabase.createClient){makeClient();return Promise.resolve(true)}
  if(!libLoading)libLoading=new Promise(ok=>{const sc=document.createElement('script');sc.src=SB_LIB;sc.onload=()=>ok(true);sc.onerror=()=>{sc.remove();ok(false)};document.head.appendChild(sc)})
    .then(r=>{libLoading=null;if(r&&window.supabase&&window.supabase.createClient){makeClient();return true}return false});
  return libLoading}
// fetch utilisé par Supabase ; « keepalive » quand la page se ferme, pour que le dernier envoi parte quand même
let KEEPALIVE=false;
function sbFetch(url,opts){if(KEEPALIVE&&opts&&typeof opts.body==='string'&&opts.body.length<60000)opts=Object.assign({},opts,{keepalive:true});return fetch(url,opts)}
async function checkMember(email){ // {ok, role} ; lève une erreur si la vérification n'a pas pu se faire
  const {data,error,status}=await sb.from('members').select('email,role').eq('email',email).maybeSingle();
  if(error){const e=new Error(error.message||'vérification impossible');e.status=status;throw e}
  return data?{ok:true,role:data.role||'member'}:{ok:false};
}
async function afterLogin(user){
  const email=normEmail(user.email);let r;
  try{r=await checkMember(email)}
  catch(e){const c=lsGet(ACC_KEY);
    if(isNetErr(e)&&accessOK(c,email))return grant(c,true);
    if(isNetErr(e))return screenOffline();
    return screenLogin({msg:"La vérification de ton accès n'a pas abouti. Réessaie dans un instant."})}
  if(!r.ok)return kickOut(email);
  grant({email,role:r.role,uid:user.id,at:Date.now()},false);
}
async function kickOut(email){ // n'est plus dans la liste des membres : déconnexion
  lsSet(ACC_KEY,null);try{await sb.auth.signOut({scope:'local'})}catch(e){}
  screenLogin({removed:email});
}
function grant(acc,offline){
  const was=AUTH.uid;
  AUTH={ok:true,email:acc.email,role:acc.role,uid:acc.uid,offline};
  lsSet(ACC_KEY,{email:acc.email,role:acc.role,uid:acc.uid,at:acc.at||Date.now()});ssSet(PEND_KEY,null);
  if(was&&was!==acc.uid){location.replace(location.pathname);return}
  document.body.classList.remove('locked');buildTabs();
  startApp();
}

/* ---------- progression synchronisée (table progress) ----------
   La copie locale (clé annales-tours) est toujours écrite. L'envoi au compte part ~2 s après la
   dernière action, et tout de suite quand la page est masquée ou fermée. Hors ligne : on garde en
   local et on renvoie au retour du réseau. Conflit entre appareils : la version la plus récente
   (updated_at = moment de la dernière modification) gagne ; le serveur ignore une écriture plus ancienne. */
const SYNC_KEY='annales-tours-sync'; // {uid, t : dernière modification, dirty : pas encore envoyée, base : déjà synchronisé sur cet appareil}
const TXT_OK='Progression sauvegardée sur ton compte',TXT_OFF='Hors ligne : sauvegarde en attente';
let syncReady=false,pushTimer=null,retryTimer=null,pushing=null,pushAgain=false;
const syncMeta=()=>{const m=lsGet(SYNC_KEY);return m&&m.uid===AUTH.uid?m:null};
const setMeta=m=>lsSet(SYNC_KEY,Object.assign({},m,{uid:AUTH.uid}));
function hasLocalSave(){const s=lsGet('annales-tours');return !!(s&&s.ans)}
function syncTouch(){if(!AUTH.ok)return;const m=syncMeta()||{base:false};setMeta(Object.assign(m,{t:Date.now(),dirty:true}));
  clearTimeout(pushTimer);pushTimer=setTimeout(push,2000)}
function scheduleRetry(fn){if(!retryTimer)retryTimer=setTimeout(()=>{retryTimer=null;fn()},30000)}
async function fetchRemote(){
  const q=sb.from('progress').select('state,updated_at').eq('user_id',AUTH.uid).maybeSingle();
  const r=await Promise.race([q,new Promise(ok=>setTimeout(()=>ok({error:{message:'network timeout'}}),10000))]);
  if(r.error)throw r.error;return r.data}
function applyRemote(st,rt){state=Object.assign(DEF_STATE(),st||{});fixState();setMeta({t:rt,dirty:false,base:true});saveLocal();applyTheme();if(view!=='quiz')render()}
function mergeInto(remote,local){const r=Object.assign(DEF_STATE(),remote||{});
  for(const k of ['ans','fav','notes','srs'])r[k]=Object.assign({},r[k],local[k]);
  if(local.run&&(!r.run||(local.run.t||0)>(r.run.t||0)))r.run=local.run;return r}
async function startApp(){
  const m=lsGet(SYNC_KEY),mine=!!(m&&m.uid===AUTH.uid),legacy=!m&&hasLocalSave();
  // sauvegarde d'un autre compte sur cet appareil : on ne la reprend pas
  if(!mine&&!legacy){state=DEF_STATE();fixState();applyTheme()}
  if(!mine)setMeta({t:0,dirty:false,base:false});
  if(mine){setSync(m.dirty?TXT_OFF:TXT_OK);render()}
  else{setSync('Chargement de ta progression…');$('#view').innerHTML='<div class="empty"><b>Chargement de ta progression…</b>Un instant.</div>'}
  await syncInit();
  if(!mine&&view!=='quiz')render();
}
async function syncInit(){
  if(!await ensureSb()){setSync(TXT_OFF);scheduleRetry(syncInit);return}
  let row;try{row=await fetchRemote()}catch(e){setSync(TXT_OFF);if(!isNetErr(e))recheck();scheduleRetry(syncInit);return}
  const m=syncMeta()||{t:0,dirty:false,base:false};syncReady=true;
  if(row){const rt=Date.parse(row.updated_at);
    if(m.base&&m.dirty&&m.t>rt)return push();                      // cet appareil a plus récent : on l'envoie
    if(!m.base&&m.dirty){state=mergeInto(row.state,state);fixState(); // changements faits ici avant la première synchro
      setMeta({t:Date.now(),dirty:true,base:true});saveLocal();if(view!=='quiz')render();return push()}
    if(!m.base||rt!==m.t)applyRemote(row.state,rt);
    setSync(TXT_OK);return}
  // pas encore de ligne : on part de la sauvegarde locale éventuelle et on crée la ligne
  setMeta({t:m.dirty?m.t:Date.now(),dirty:true,base:true});return push();
}
async function push(){
  if(!syncReady||!AUTH.ok||!sb)return;
  if(pushing){pushAgain=true;return pushing}
  const m=syncMeta();if(!m||!m.dirty){setSync(TXT_OK);return}
  clearTimeout(pushTimer);
  pushing=(async()=>{try{
      const t=m.t;
      const {data,error}=await sb.from('progress').upsert({user_id:AUTH.uid,state,updated_at:new Date(t).toISOString()},{onConflict:'user_id'}).select('updated_at');
      if(error)throw error;
      if(!data||!data.length){ // refusé : un autre appareil a une version plus récente, elle gagne
        const row=await fetchRemote();if(row)applyRemote(row.state,Date.parse(row.updated_at))}
      else{const m2=syncMeta();if(m2)setMeta(Object.assign(m2,{base:true},m2.t===t?{dirty:false}:{}))}
      setSync(TXT_OK);clearTimeout(retryTimer);retryTimer=null;
    }catch(e){setSync(TXT_OFF);if(e&&(e.status===401||/jwt/i.test(e.message||'')))recheck();scheduleRetry(push)}})();
  try{await pushing}finally{pushing=null}
  if(pushAgain){pushAgain=false;const m3=syncMeta();if(m3&&m3.dirty)return push()}
}
async function pullNewer(){ // retour sur l'onglet : un autre appareil a-t-il avancé ?
  if(!syncReady||!AUTH.ok||pushing)return;const m=syncMeta()||{};if(m.dirty)return push();
  try{const row=await fetchRemote();if(row){const rt=Date.parse(row.updated_at);if(rt>(m.t||0))applyRemote(row.state,rt)}setSync(TXT_OK)}
  catch(e){if(!navigator.onLine)setSync(TXT_OFF)}}
function flushNow(){if(!AUTH.ok)return;saveLocal();const m=syncMeta();
  if(m&&m.dirty&&syncReady){KEEPALIVE=true;push().finally(()=>{KEEPALIVE=false})}}
async function syncPending(){const m=syncMeta();if(!m||!m.dirty)return false;await push();const m2=syncMeta();return !!(m2&&m2.dirty)}
function clearLocalProgress(){AUTH.ok=false;clearTimeout(saveTimer);clearTimeout(pushTimer);lsSet(SYNC_KEY,null);try{localStorage.removeItem('annales-tours')}catch(e){}}
document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')flushNow();else pullNewer()});
addEventListener('pagehide',flushNow);
addEventListener('online',()=>{if(!AUTH.ok)return;if(syncReady)push();else syncInit()});
addEventListener('offline',()=>{const m=syncMeta();if(AUTH.ok&&m&&m.dirty)setSync(TXT_OFF)});
function screenOffline(){
  const box=authScreen(`<section class="panel"><h2>Connexion impossible</h2><p>Atlas n'arrive pas à joindre le service de connexion. Il faut être en ligne pour te connecter.</p><div><button class="primary" type="button" id="retry">Réessayer</button></div></section>`);
  box.querySelector('#retry').onclick=()=>location.reload();
}

/* ---------- écran de connexion ---------- */
function screenLogin(o){
  o=o||{};const pend=ssGet(PEND_KEY);
  if(pend&&pend.email&&!o.refused&&!o.removed&&!o.email)return screenCode(pend.email,o.msg);
  const box=authScreen(`<section class="panel">
    <div><h2>Connexion</h2><p class="muted">Atlas est réservé aux membres inscrits.</p></div>
    ${o.refused?`<p class="amsg bad" role="alert"><b>${esc(MSG_NOT_MEMBER)}</b><br>${esc(o.refused)}. Vérifie l'adresse, ou demande à ${esc(CONTACT())} de t'ajouter.</p>`:''}
    ${o.removed?`<p class="amsg bad" role="alert"><b>Ta session a été fermée.</b><br>${esc(o.removed)} n'est plus dans la liste des membres. Si c'est une erreur, contacte ${esc(CONTACT())}.</p>`:''}
    ${o.msg?`<p class="amsg" role="alert">${esc(o.msg)}</p>`:''}
    <form id="fEmail" novalidate><div class="field"><label for="aEmail">Ton adresse e-mail</label><input type="email" id="aEmail" autocomplete="email" inputmode="email" autocapitalize="off" spellcheck="false" required value="${esc(o.email||o.refused||'')}"></div>
     <button class="primary" type="submit" id="aSend">Recevoir un code</button></form>
    <p class="muted small">Tu reçois un code par e-mail. Pas de mot de passe.</p>
    <div><button class="linkbtn" type="button" id="aHave">J'ai déjà un code</button></div>
   </section>`);
  const f=box.querySelector('#fEmail'),inp=box.querySelector('#aEmail');
  if(matchMedia('(hover:hover)').matches)inp.focus();
  box.querySelector('#aHave').onclick=()=>{const email=normEmail(inp.value);
    if(!EMAIL_RE.test(email)){showMsg(box,"Écris d'abord ton adresse e-mail, puis touche « J'ai déjà un code ».");inp.focus();return}
    ssSet(PEND_KEY,{email,at:Date.now()});screenCode(email)};
  f.onsubmit=async e=>{e.preventDefault();const email=normEmail(inp.value);
    if(!EMAIL_RE.test(email)){showMsg(box,"Cette adresse e-mail n'a pas l'air valide.");return}
    const bt=box.querySelector('#aSend');bt.disabled=true;bt.textContent='Vérification…';
    const r=await sendCode(email);bt.disabled=false;bt.textContent='Recevoir un code';
    if(r.refused)return screenLogin({refused:email});
    if(r.msg)return showMsg(box,r.msg);
    screenCode(email)};
}
async function sendCode(email){ // {ok} | {refused} | {msg}
  const OFF='Le service de connexion ne répond pas. Vérifie ta connexion internet, puis réessaie.';
  try{const {data,error}=await sb.rpc('can_join',{e:email});
    if(error)return{msg:isNetErr(error)?OFF:"La vérification de l'adresse n'a pas abouti. Réessaie dans un instant."};
    if(data!==true)return{refused:true}}
  catch(e){return{msg:OFF}}
  try{const {error}=await sb.auth.signInWithOtp({email,options:{shouldCreateUser:true,emailRedirectTo:location.origin+location.pathname}});
    if(error){const m=String(error.message||''),w=(m.match(/(\d+)\s*seconds?/)||[])[1];
      if(error.status===429||w)return{msg:w?`Un code vient d'être envoyé. Attends ${w} secondes avant d'en redemander un.`:'Trop de demandes de code. Attends quelques minutes, puis réessaie.'};
      return{msg:isNetErr(error)?OFF:"L'e-mail n'a pas pu partir. Réessaie dans un instant."}}}
  catch(e){return{msg:"L'e-mail n'a pas pu partir. Réessaie dans un instant."}}
  ssSet(PEND_KEY,{email,at:Date.now()});return{ok:true};
}
function screenCode(email,msg){
  const box=authScreen(`<section class="panel">
    <div><h2>Vérifie tes e-mails</h2><p class="muted">On a envoyé un code à <b>${esc(email)}</b>. Il peut mettre une minute à arriver. Regarde aussi dans les indésirables.</p></div>
    ${msg?`<p class="amsg" role="alert">${esc(msg)}</p>`:''}
    <form id="fCode" novalidate><div class="field"><label for="aCode">Code reçu par e-mail</label><input type="text" id="aCode" inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]*" maxlength="10" required></div>
     <button class="primary" type="submit" id="aOk">Se connecter</button></form>
    <div class="row" style="gap:18px"><button class="linkbtn" type="button" id="aResend">Renvoyer un code</button><button class="linkbtn" type="button" id="aBack">Changer d'adresse</button></div>
   </section>`);
  const f=box.querySelector('#fCode'),inp=box.querySelector('#aCode');inp.focus();
  inp.oninput=()=>{const v=inp.value.replace(/\D/g,'').slice(0,10);if(v!==inp.value)inp.value=v};
  f.onsubmit=async e=>{e.preventDefault();const token=inp.value.replace(/\D/g,'');
    if(token.length<6||token.length>10){showMsg(box,'Le code fait de 6 à 10 chiffres. Recopie-le en entier.');return}
    const bt=box.querySelector('#aOk');bt.disabled=true;bt.textContent='Connexion…';
    let res;try{res=await sb.auth.verifyOtp({email,token,type:'email'})}catch(x){res={error:x}}
    bt.disabled=false;bt.textContent='Se connecter';
    if(res.error||!res.data||!res.data.session){showMsg(box,res.error&&isNetErr(res.error)?'Pas de connexion internet. Réessaie une fois en ligne.':'Code incorrect ou expiré. Prends le dernier e-mail reçu, ou demande un nouveau code.','bad');inp.select();return}
    ssSet(PEND_KEY,null);afterLogin(res.data.session.user)};
  box.querySelector('#aResend').onclick=async()=>{const r=await sendCode(email);if(r.refused)return screenLogin({refused:email});showMsg(box,r.msg||'Nouveau code envoyé. Prends le dernier e-mail reçu.',r.msg?'':'ok')};
  box.querySelector('#aBack').onclick=()=>{ssSet(PEND_KEY,null);screenLogin({email})};
}

/* ---------- vérifications suivantes ---------- */
async function recheck(){ // retour en ligne ou retour sur l'onglet : session et accès toujours valables ?
  if(!AUTH.ok||!await ensureSb())return;const c=lsGet(ACC_KEY);if(!AUTH.offline&&c&&Date.now()-c.at<6*3600e3)return;
  let r;try{const s=await sb.auth.getSession();
    if(!(s.data&&s.data.session)){if((s.error&&isNetErr(s.error))||!navigator.onLine)return;lsSet(ACC_KEY,null);return screenLogin({msg:'Ta session a expiré : reconnecte-toi.'})}
    r=await checkMember(AUTH.email)}catch(e){return}
  if(!r.ok)return kickOut(AUTH.email);
  lsSet(ACC_KEY,{email:AUTH.email,role:r.role,uid:AUTH.uid,at:Date.now()});
  const was=AUTH.role;AUTH.offline=false;AUTH.role=r.role;
  if(was!==r.role){buildTabs();if(view!=='quiz')render()}
}
addEventListener('online',()=>recheck());
document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')recheck()});

/* ---------- onglets ---------- */
const IC_MEMB='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18.5 14.5A6.5 6.5 0 0 1 21.5 20"/></svg>';
function buildTabs(){const nav=$('#tabs');let a=nav.querySelector('a[href="#membres"]');
  if(isAdmin()&&!a)nav.insertAdjacentHTML('beforeend',`<a href="#membres">${IC_MEMB}Membres</a>`);
  if(!isAdmin()&&a)a.remove()}

/* ---------- Réglages : compte ---------- */
function compteHTML(){
  if(!AUTH.ok)return'';
  return `<div class="panel"><h3 style="margin-bottom:6px">Compte</h3><p style="margin:0 0 4px">Connecté avec <b>${esc(AUTH.email)}</b>${isAdmin()?' · administration':''}</p>
   <p class="muted" style="margin:0 0 12px">${AUTH.offline?'Hors ligne pour le moment. ':''}Se déconnecter efface ta progression de cet appareil. Elle reste sur ton compte.</p>
   <div id="outZone"><button id="signOut">Se déconnecter</button></div></div>`}
function wireCompte(el){const b=el.querySelector('#signOut');if(b)b.onclick=()=>signOut(false)}
async function signOut(force){
  if(!force&&typeof syncPending==='function'&&await syncPending()){
    const z=$('#outZone');if(!z)return;
    z.innerHTML='<p style="margin:0 0 10px">Hors ligne : ta dernière progression n\'est pas encore sur ton compte. Si tu te déconnectes maintenant, elle sera perdue. Continuer ?</p><div class="row"><button class="danger" id="outY">Me déconnecter quand même</button><button id="outN">Annuler</button></div>';
    $('#outY').onclick=()=>signOut(true);$('#outN').onclick=()=>render();return}
  lsSet(ACC_KEY,null);ssSet(PEND_KEY,null);
  if(typeof clearLocalProgress==='function')clearLocalProgress();
  try{if(sb)await sb.auth.signOut({scope:'local'})}catch(e){}
  location.replace(location.pathname);
}

/* ---------- signalements (table reports) ----------
   Un signalement est un simple message pour l'équipe : il ne modifie jamais une correction. */
async function sendReport(qid,message){
  if(!AUTH.ok||!await ensureSb())throw new Error('hors ligne');
  const {error}=await sb.from('reports').insert({user_id:AUTH.uid,question_id:qid,message:String(message).slice(0,2000)});
  if(error)throw error}
const qRef=q=>q?sess(q)+' · '+q.mod+' · Q'+q.q:'';
function showQuestion(id){const q=BYID[id];if(!q){toast('Question introuvable');return}
  // aperçu en lecture : correction affichée, rien n'est compté dans les statistiques
  run={ids:[id],i:0,from:'membres',label:'Signalement',mode:'fin',sel:{},res:{},done:true,summary:false,confirm:false,chrono:false,limit:60,el:0};go('quiz')}
async function loadReports(){const box=$('#reps');if(!box)return;
  const {data,error}=await sb.from('reports').select('id,question_id,message,created_at,done').order('created_at',{ascending:false}).limit(300);
  if(!$('#reps'))return;
  if(error){box.innerHTML='<small>Signalements injoignables pour le moment.</small>';return}
  const L=(data||[]).sort((a,b)=>a.done-b.done),open=L.filter(r=>!r.done).length;
  $('#repN').textContent=open?open+' à traiter':'Rien à traiter';
  box.innerHTML=L.length?L.map(r=>{const q=BYID[r.question_id];return `<div class="rp${r.done?' done':''}"><span><b>${esc(q?qRef(q):r.question_id)}</b>${q?' · '+esc(q.mat):''}${r.done?' <span class="chip ok">traité</span>':''}</span>
    <span>${esc(r.message)}</span><small>${new Date(r.created_at).toLocaleDateString('fr-FR')}</small>
    <div class="row">${q?`<button class="sm" data-see="${esc(r.question_id)}">Voir la question</button>`:''}<button class="sm${r.done?' ghost':''}" data-done="${esc(r.id)}" data-v="${r.done?0:1}">${r.done?'Rouvrir':'Traité'}</button></div></div>`}).join(''):'<small>Aucun signalement pour l\'instant.</small>';
  box.querySelectorAll('[data-see]').forEach(b=>b.onclick=()=>showQuestion(b.dataset.see));
  box.querySelectorAll('[data-done]').forEach(b=>b.onclick=async()=>{b.disabled=true;
    const {error}=await sb.from('reports').update({done:b.dataset.v==='1'}).eq('id',b.dataset.done);
    if(error){toast('Modification impossible');b.disabled=false;return}loadReports()})}

/* ---------- onglet Membres (administrateurs) ---------- */
const MV={list:null,err:'',q:'',prev:null};
async function loadMembers(){const {data,error}=await sb.from('members').select('email,role,note,added_at').order('email');if(error)throw error;MV.list=data||[]}
// Colle une colonne d'e-mails ou un CSV : on garde ce qui ressemble à une adresse, en minuscules, sans doublon.
function parseEmails(raw,existing){
  const seen=new Set(),neu=[],have=[],bad=[];let dup=0,skipped=0;
  for(const line of String(raw||'').split(/\r?\n/)){if(!line.trim())continue;
    const em=line.split(/[\s,;|]+/).map(t=>t.replace(/^mailto:/i,'').replace(/^[<"'(\[]+|[>"')\].]+$/g,'')).filter(t=>t.includes('@'));
    if(!em.length){skipped++;continue}
    for(const x of em){const e=x.toLowerCase();if(!EMAIL_RE.test(e)){bad.push(x);continue}
      if(seen.has(e)){dup++;continue}seen.add(e);(existing.has(e)?have:neu).push(e)}}
  return {neu,have,bad,dup,skipped}}
function vMembres(el){
  if(!sb){el.innerHTML='<div class="empty"><b>Hors ligne</b>La liste des membres n\'est disponible qu\'en ligne.</div>';return}
  if(!MV.list){el.innerHTML='<div class="head"><div><h2>Membres</h2><p class="muted" style="margin:0">Chargement de la liste…</p></div></div>';
    loadMembers().then(()=>{MV.err=''}).catch(e=>{MV.err=isNetErr(e)?'Pas de connexion : la liste n\'est disponible qu\'en ligne.':'La liste n\'a pas pu être lue.'})
      .then(()=>{if(view==='membres'){if(!MV.list)MV.list=[];render();if(MV.err)MV.list=null}});return}
  const na=MV.list.filter(m=>m.role==='admin').length,P=MV.prev;
  el.innerHTML=`<div class="head"><div><h2>Membres</h2><p class="muted" style="margin:0">${MV.list.length} adresse${MV.list.length>1?'s':''} sur la liste · ${na} admin${na>1?'s':''}</p></div></div>
  <div class="stack" style="max-width:860px">
   ${MV.err?`<div class="notice bad"><b>${esc(MV.err)}</b></div>`:''}
   <div class="panel"><h3 style="margin-bottom:6px">Ajouter depuis un tableur</h3>
    <p class="muted" style="margin:0 0 12px">Colle une colonne d'e-mails ou un CSV. Les adresses sont mises en minuscules, sans espaces ni doublons. Aucun e-mail n'est envoyé : préviens les membres toi-même.</p>
    ${P?`<div class="stack" style="gap:10px">
      <p style="margin:0"><b>${P.neu.length} nouvelle${P.neu.length>1?'s':''} adresse${P.neu.length>1?'s':''}</b>${P.have.length?` · ${P.have.length} déjà sur la liste`:''}${P.dup?` · ${P.dup} doublon${P.dup>1?'s':''} retiré${P.dup>1?'s':''}`:''}${P.skipped?` · ${P.skipped} ligne${P.skipped>1?'s':''} sans adresse ignorée${P.skipped>1?'s':''}`:''}${P.note?` · note « ${esc(P.note)} »`:''}</p>
      ${P.bad.length?`<div class="notice bad"><b>${P.bad.length} adresse${P.bad.length>1?'s':''} invalide${P.bad.length>1?'s':''}, non ajoutée${P.bad.length>1?'s':''} :</b> ${P.bad.map(esc).join(', ')}</div>`:''}
      ${P.neu.length?`<div class="mprev">${P.neu.map(esc).join('<br>')}</div>`:''}
      <div class="row"><button class="primary" id="mOk" ${P.neu.length?'':'disabled'}>Ajouter ${P.neu.length} membre${P.neu.length>1?'s':''}</button><button id="mBack">Modifier</button><span class="muted" id="mRes" role="status"></span></div></div>`
    :`<div class="stack mimp" style="gap:10px"><div class="field"><label for="mAdd">Adresses e-mail</label><textarea id="mAdd" rows="6" autocapitalize="off" spellcheck="false" placeholder="prenom.nom@exemple.fr">${esc(MV.raw||'')}</textarea></div>
      <div class="field" style="max-width:260px"><label for="mNote">Note pour toutes (facultatif)</label><input type="text" id="mNote" placeholder="ex. 2026-2027" value="${esc(MV.note||'')}" autocomplete="off"></div>
      <div class="row"><button class="primary" id="mCheck">Voir l'aperçu</button><span class="muted" id="mRes" role="status"></span></div></div>`}
   </div>
   <div class="panel"><div class="row" style="justify-content:space-between"><h3>Signalements</h3><span class="muted" id="repN"></span></div>
    <p class="muted" style="margin:6px 0 0">Un signalement ne modifie jamais une correction. Vérifie dans le cours avant de corriger les données.</p>
    <div class="reports" id="reps"><small>Chargement…</small></div></div>
   <div class="panel"><div class="row" style="justify-content:space-between"><h3>Liste</h3><input type="search" id="mQ" placeholder="Chercher une adresse ou une note" aria-label="Chercher un membre" value="${esc(MV.q)}" style="flex:0 1 280px"></div>
    ${MV.list.length?`<div class="mlist">${MV.list.map(m=>{const me=m.email===AUTH.email;return `<div class="mrow" data-s="${esc(m.email+' '+(m.note||'').toLowerCase())}">
      <span class="me">${esc(m.email)}${m.role==='admin'?' <span class="chip plain" style="background:var(--navy-soft);color:var(--navy)">admin</span>':''}${me?' <span class="chip plain">toi</span>':''}<small>ajouté le ${m.added_at?new Date(m.added_at).toLocaleDateString('fr-FR'):'?'}</small></span>
      <input type="text" data-note="${esc(m.email)}" value="${esc(m.note||'')}" placeholder="Note" aria-label="Note pour ${esc(m.email)}" autocomplete="off">
      ${me?'<span></span>':`<div class="macts"><button class="sm ghost" data-role="${esc(m.email)}" data-to="${m.role==='admin'?'member':'admin'}">${m.role==='admin'?'Retirer admin':'Rendre admin'}</button><button class="sm ghost" data-del="${esc(m.email)}" style="color:var(--bad)">Retirer</button></div>`}</div>`}).join('')}</div>
      <p class="muted" id="mNone" style="margin:10px 0 0" hidden>Aucune adresse ne correspond.</p>`:'<p class="muted" style="margin:10px 0 0">Personne sur la liste.</p>'}
   </div></div>`;
  loadReports();
  const qi=$('#mQ'),filt=()=>{const q=normEmail(qi.value);MV.q=qi.value;let n=0;el.querySelectorAll('.mrow').forEach(r=>{const h=!!q&&!r.dataset.s.includes(q);r.hidden=h;if(!h)n++});const z=$('#mNone');if(z)z.hidden=!!n||!MV.list.length};
  qi.oninput=filt;filt();
  if($('#mCheck'))$('#mCheck').onclick=()=>{MV.raw=$('#mAdd').value;MV.note=$('#mNote').value.trim();
    const r=parseEmails(MV.raw,new Set(MV.list.map(m=>m.email)));
    if(!r.neu.length&&!r.have.length&&!r.bad.length){$('#mRes').textContent='Aucune adresse trouvée dans ce texte.';return}
    MV.prev=Object.assign(r,{note:MV.note});render()};
  if($('#mBack'))$('#mBack').onclick=()=>{MV.prev=null;render()};
  if($('#mOk'))$('#mOk').onclick=async()=>{const b=$('#mOk');b.disabled=true;const rows=P.neu.map(email=>({email,note:P.note||null}));let err=null;
    for(let i=0;i<rows.length&&!err;i+=500){$('#mRes').textContent=`Ajout… ${Math.min(i+500,rows.length)} / ${rows.length}`;
      ({error:err}=await sb.from('members').upsert(rows.slice(i,i+500),{onConflict:'email',ignoreDuplicates:true}))}
    try{await loadMembers()}catch(e){}
    if(err){MV.prev=null;MV.err=isNetErr(err)?'Pas de connexion : une partie des adresses n\'a peut-être pas été ajoutée. Vérifie la liste.':'L\'ajout a échoué : '+(err.message||'erreur');render();return}
    MV.prev=null;MV.raw='';MV.note='';MV.err='';render();toast(rows.length+(rows.length>1?' membres ajoutés':' membre ajouté'))};
  el.querySelectorAll('[data-note]').forEach(i=>i.onchange=async()=>{const v=i.value.trim()||null;
    const {error}=await sb.from('members').update({note:v}).eq('email',i.dataset.note);
    if(error){toast('Note non enregistrée');return}const m=MV.list.find(x=>x.email===i.dataset.note);if(m)m.note=v;
    i.closest('.mrow').dataset.s=i.dataset.note+' '+(v||'').toLowerCase();toast('Note enregistrée')});
  // rôle admin : confirmation en deux clics ; on ne peut pas changer son propre rôle (pas de bouton sur sa ligne), donc jamais zéro admin
  el.querySelectorAll('[data-role]').forEach(b=>{let armed=false;b.onclick=async()=>{const to=b.dataset.to,em=b.dataset.role;
    if(!armed){armed=true;b.textContent=to==='admin'?'Confirmer : admin':'Confirmer : membre';return}
    b.disabled=true;const {error}=await sb.from('members').update({role:to}).eq('email',em);
    if(error){toast('Le changement de rôle a échoué');b.disabled=false;armed=false;b.textContent=to==='admin'?'Rendre admin':'Retirer admin';return}
    const m=MV.list.find(x=>x.email===em);if(m)m.role=to;render();toast(to==='admin'?em+' est maintenant admin':em+' n\'est plus admin')}});
  el.querySelectorAll('[data-del]').forEach(b=>{let armed=false;b.onclick=async()=>{
    if(!armed){armed=true;b.textContent='Confirmer le retrait';return}
    b.disabled=true;const {error}=await sb.from('members').delete().eq('email',b.dataset.del);
    if(error){toast('Le retrait a échoué');b.disabled=false;return}
    MV.list=MV.list.filter(x=>x.email!==b.dataset.del);b.closest('.mrow').remove();
    const h=el.querySelector('.head p');if(h)h.textContent=h.textContent.replace(/^\d+ adresses?/,n=>{const k=MV.list.length;return k+' adresse'+(k>1?'s':'')});toast('Retiré de la liste')}});
}

bootCompte();
