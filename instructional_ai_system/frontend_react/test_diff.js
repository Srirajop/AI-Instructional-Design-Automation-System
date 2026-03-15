import * as Diff from 'diff';

const oldText = "| Screen | Text | Narration |\n|---|---|---|\n| 1.1 | Welcome | Hello |\n| 1.2 | Overview | This is an overview |\n";
const newText = "| Screen | Text | Narration |\n|---|---|---|\n| 1.1 | Welcome | Hello |\n| 1.2 | Overview | This is a creative overview |\n";

const diff = Diff.diffWords(oldText, newText);
const diffMarkup = diff.map(part => {
    if (!part.added && !part.removed) return part.value;

    const tag = part.added ? 'ins' : 'del';
    return part.value.split(/([|\n]|\|[\s\-:|]+\|)/).map(seg => {
        if (!seg) return '';
        if (/^([|\n]|\|[\s\-:|]+\|)$/.test(seg)) return seg;
        return `<${tag}>${seg}</${tag}>`;
    }).join('');
}).join('');

console.log("====== DIFF MARKUP ======");
console.log(diffMarkup);

// Simulate cleanMarkdown
const cleanMarkdown = (text) => {
    const lines = text.split('\n');
    const normalized = [];
    for (let i = 0; i < lines.length; i++) {
        let row = lines[i].trim();
        if (row.split('|').length >= 3) {
            if (!row.startsWith('|')) row = '| ' + row;
            if (!row.endsWith('|')) row = row + ' |';
            normalized.push(row);
        } else {
            normalized.push(lines[i]);
        }
    }
    return normalized.join('\n');
};

console.log("\n====== AFTER CLEANER ======");
console.log(cleanMarkdown(diffMarkup));
