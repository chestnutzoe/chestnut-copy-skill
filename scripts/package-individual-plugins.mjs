// Release copies ONLY from the public bundle. Never reads private Chestnut files.
import {readFileSync,writeFileSync,mkdirSync,cpSync,readdirSync} from 'node:fs';
const root = new URL('../',import.meta.url);
const read = path => JSON.parse(readFileSync(new URL(path,root)));
const write = (path,value) => writeFileSync(new URL(path,root),JSON.stringify(value,null,2)+'\n');
const bundle = read('plugins/chestnut/.codex-plugin/plugin.json');
const names = {
  'chestnut-brand-story':'个人品牌故事',
  'chestnut-positioning-statement':'一句话定位',
  'chestnut-brand-guidance':'品牌表达指南',
  'chestnut-product-brief':'产品说明书',
  'chestnut-style-analyzer':'文风分析',
  'chestnut-copy-sop':'文案工作流',
  'chestnut-wechat-publisher':'公众号草稿发布'
};
const claude = read('.claude-plugin/marketplace.json');
claude.description = 'Chestnut creator toolkit: install the complete bundle or individual skills.';
claude.plugins = claude.plugins.filter(p => !Object.hasOwn(names,p.name));
claude.plugins[0].description = bundle.description;
for (const [name,label] of Object.entries(names)) {
  const target = `plugins/${name}`;
  if(!readdirSync(new URL('plugins/',root)).includes(name))throw Error('Scaffold plugin first: '+name);
  mkdirSync(new URL(`${target}/skills/`,root),{recursive:true});
  cpSync(new URL(`plugins/chestnut/skills/${name}`,root),new URL(`${target}/skills/${name}`,root),{recursive:true});
  const description = `Chestnut ${label}：独立安装的公开版 Skill。`;
  write(`${target}/.codex-plugin/plugin.json`,{...bundle,name,description,interface:{...bundle.interface,displayName:`Chestnut · ${label}`,shortDescription:description,longDescription:description,defaultPrompt:[`使用 ${name} 帮我完成${label}。`]}});
  mkdirSync(new URL(`${target}/.claude-plugin/`,root),{recursive:true});
  write(`${target}/.claude-plugin/plugin.json`,{name,version:bundle.version,description,author:bundle.author,license:bundle.license});
  claude.plugins.push({name,description,source:`./${target}`,category:'productivity'});
}
write('.claude-plugin/marketplace.json',claude);
console.log('Packaged 7 independent plugins from the public bundle.');
