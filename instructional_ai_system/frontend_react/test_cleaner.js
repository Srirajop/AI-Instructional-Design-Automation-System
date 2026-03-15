const oldText = `| Screen | Text | Narration |\n|---|---|---|\n| 1.1 | Welcome | Hello |\n| 1.2 | Overview | This is an overview |`;
const newText = `| Screen | Text | Narration |\n|---|---|---|\n| 1.1 | Welcome | Hello |\n| 1.2 | Overview | This is a NEW overview |`;

import * as Diff from 'diff';

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

console.log("=== RAW DIFF ===");
console.log(diffMarkup);

const cleanMarkdown = (text) => {
    let cleaned = (text || '')
        .replace(/^[=]{5,}$/gm, '')
        .replace(/^-{5,}$/gm, '')
        .replace(/---\s*START OF DOCUMENT\s*---/gi, '')
        .replace(/---\s*END OF DOCUMENT\s*---/gi, '')
        .replace(/\s*\[START CONTENT\]\s*/gi, '')
        .replace(/\s*\[END CONTENT\]\s*/gi, '')
        .replace(/^\*\*(Project Information|Course Overview|Learning Objectives|Module Breakdown|Instructional Strategy|Assessment Strategy|Technical Specifications)\*\*\s*$/gmi, '')
        .replace(/^#+\s*(Project Information|Course Overview|Learning Objectives|Module Breakdown|Instructional Strategy|Assessment Strategy|Technical Specifications)\s*$/gmi, '')
        .replace(/\n{5,}/g, '\n\n\n');

    cleaned = cleaned.replace(/^(#{1,6})\s*(\|.+\|)\s*$/gm, '$2');
    cleaned = cleaned.replace(/^\*\*(\|.+\|)\*\*\s*$/gm, '$1');

    const lines = cleaned.split('\n');
    const normalized = [];
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();
        if (line.split('|').length >= 3) {
            let row = line;
            if (!row.startsWith('|')) row = '| ' + row;
            if (!row.endsWith('|')) row = row + ' |';
            normalized.push(row);
        } else {
            normalized.push(lines[i]);
        }
    }
    return normalized.join('\n');
};

console.log("\n=== CLEANED DIFF ===");
console.log(cleanMarkdown(diffMarkup));
