export class TextScramble {
  constructor(el) {
    this.el = el;
    this.update = this.update.bind(this);
    this.deleteText = this.deleteText.bind(this);
    this.typeText = this.typeText.bind(this);
  }

  setText(newText) {
    this.newText = newText;
    this.oldText = this.el.innerText;
    this.promise = new Promise((resolve) => this.resolve = resolve);

    this.deleteText();
    return this.promise;
  }

  deleteText() {
    const length = this.oldText.length;
    this.queue = [];
    for (let i = length; i >= 0; i--) {
      this.queue.push({ text: this.oldText.slice(0, i), start: (length - i) * 4, end: (length - i + 1) * 4 });
    }
    this.frame = 0;
    this.update(this.typeText);
  }

  typeText() {
    const length = this.newText.length;
    this.queue = [];
    for (let i = 0; i <= length; i++) {
      this.queue.push({ text: this.newText.slice(0, i), start: i * 4, end: (i + 1) * 4 });
    }
    this.frame = 0;
    this.update();
  }

  update(nextStep = null) {
    let output = '';
    let complete = 0;
    for (let i = 0, n = this.queue.length; i < n; i++) {
      let { text, start, end } = this.queue[i];
      if (this.frame >= end) {
        complete++;
        output = text;
      } else if (this.frame >= start) {
        output = text;
        break;
      }
    }

    this.el.innerHTML = output;
    if (complete === this.queue.length) {
      if (nextStep) {
        nextStep(); 
      } else {
        this.resolve();
      }
    } else {
      this.frameRequest = requestAnimationFrame(() => this.update(nextStep));
      this.frame++;
    }
  }
}