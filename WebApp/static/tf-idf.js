

function tokenize(document) {
    let punctuation = '!@#$%^&*()=-+_{}[]\|;:",.<>/?';
    for (let p of punctuation) {
        document = document.replace(p, '');
    }
    document.replace('\n', ' ');
    let updated_words = document.split(' ');
    return updated_words;
}

function compute_idfs(documents) {
    var values = {};
    for (const [key, value] of Object.entries(documents)) {
        let words = new Set();
        for (let word of value){
            if (!words.has(word)){
                words.add(word);
                try {
                    values[word] += 1;
                }
                catch (err) {
                    values[word] = 1;
                }
            }
        }
    }
    var idfs = {};
    for (const [key, value] of Object.entries(values)) {
        idfs[key] = Math.log(documents.length / value);
    }
    return idfs;
}

function sorted(items, kwargs = {}) {
    const key = kwargs.key === undefined ? x => x : kwargs.key;
    const reverse = kwargs.reverse === undefined ? false : kwargs.reverse;
    const sortKeys = items.map((item, pos) => [key(item), pos]);
    const comparator =
        Array.isArray(sortKeys[0][0])
            ? ((left, right) => {
                for (var n = 0; n < Math.min(left.length, right.length); n++) {
                    const vLeft = left[n], vRight = right[n];
                    const order = vLeft == vRight ? 0 : (vLeft > vRight ? 1 : -1);
                    if (order != 0) return order;
                }
                return left.length - right.length;
            })
            : ((left, right) => {
                const vLeft = left[0], vRight = right[0];
                const order = vLeft == vRight ? 0 : (vLeft > vRight ? 1 : -1);
                return order;
            });
    sortKeys.sort(comparator);
    if (reverse) sortKeys.reverse();
    return sortKeys.map((order) => items[order[1]]);
}

function count(item, array) {
    let total = 0;
    for (const ele of array) {
        if (item == ele) {
            total += 1;
        }
    }
    return total
}

function top_sentences(query, sentences, idfs) {
    let ranks = [];

    for (const [key, value] of Object.entries(sentences)) {
        let sentence_values = [key, 0, 0];

        for (let word of query) {
            if (value.includes(word)) {
                sentence_values[1] += idfs[word];
                sentence_values[2] += count(word, value) / value.length;
            }
        }

        ranks.push(sentence_values);
    }
    let final = [];
    for (let sentence of sorted(ranks, {key: x=>(x[1], x[2]), reverse:true})) {
        final.push(sentence[0]);
    }

    return final;
}

function main(file, query) {
    let tokenized_query = tokenize(query);

    let pages = {};
    for (let page of file.split('\n\n')) {
        let tokens = tokenize(page);
        pages[page] = tokens;
    }
    let idfs = compute_idfs(pages);

    let page_matches = top_sentences(tokenized_query, pages, idfs);

    let passages = {};
    for (let page of page_matches) {
        for (let paragraph of page.split('\n\n')) {
            tokens = tokenize(paragraph);
            passages[paragraph] = tokens;
        }
    }

    let paragraph_idfs = compute_idfs(passages);

    return top_sentences(tokenized_query, passages, paragraph_idfs);
}



function index(item, array) {
    for (let index = 0; index < array.length; index ++) {
        if (array[index] == item) {
            return index
        }
    }
    return -1
}

function get_closest_sentences(match, sentences){
    let match_pos = index(match, sentences);
    let paragraph_pos = [];
    if (match_pos == 0 || match_pos == 1) {
        paragraph_pos = [0, 1, 2, 3, 4];
    } else if (match_pos == sentences.length || match_pos == sentences.length - 1) {
        paragraph_pos = [match_pos-4, match_pos-3, match_pos-2, match_pos+1, match_pos];
    } else {
        paragraph_pos = [match_pos-2, match_pos-1, match_pos, match_pos+1, match_pos+2];
    }
    let new_text = '';
    for (let pos of paragraph_pos) {
        new_text += sentences[pos];
    }
    return new_text;
}