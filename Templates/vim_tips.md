[header]: # (To generate a html version of this document:)
[pandoc]: # (pandoc vim_tips.md -c github.css -o vim_tips.html -s --self-contained)

# A Beginner's Guide to Vim

Vim is the editor of choice for many developers and power users. It's a "modal" text editor.

What the heck do we mean by "modal"? In Vim, the mode that the editor is in determines whether the alphanumeric keys will input those characters or move the cursor through the document.

---

Vim has three operating modes, but in this tiny guide we will focus only in two of them: **command mode** & **insert mode**.

When you run `vim` in the Terminal to edit a file, it starts out in command mode.

```
Under command mode:
    use the 'h', 'j', 'k', and 'l' keys to move your cursor left, down, up, and right
    hit the 'i' key to switch to edit mode

Under insert mode:
    you can use Vim as a regular text editor
    use the 'left', 'down', 'up', and 'right' arrows to move your cursor
    hit the 'Esc' key to switch back to edit mode

Under command mode again:
    once you are done editing, press 'shift + z + z' for quick save & exit
```

For additional information, please refer to <https://www.linux.com/learn/vim-101-beginners-guide-vim>.

---
