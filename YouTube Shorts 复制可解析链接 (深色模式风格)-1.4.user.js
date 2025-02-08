// ==UserScript==
// @name         YouTube Shorts 复制可解析链接 (深色模式风格)
// @namespace    http://tampermonkey.net/
// @version      1.4
// @description  在 Shorts 界面的点赞按钮上方添加 YouTube 风格的 “Link” 按钮
// @match        *://www.youtube.com/shorts/*
// @run-at       document-end
// ==/UserScript==

(function() {
    'use strict';

    function addCopyButton() {
        // 先检查按钮是否已存在
        if (document.getElementById('copy-watch-link-btn')) return;

        // 获取 Shorts 界面的按钮容器
        let actionBar = document.querySelector('ytd-reel-video-renderer #actions');

        if (!actionBar) {
            // 容器可能还未加载，尝试稍后执行
            setTimeout(addCopyButton, 1000);
            return;
        }

        // 创建按钮
        let btn = document.createElement('button');
        btn.innerText = 'Link';
        btn.id = 'copy-watch-link-btn';

        // 按钮样式 (完全匹配 YouTube 默认圆形按钮)
        btn.style.width = '50px';
        btn.style.height = '50px';
        btn.style.backgroundColor = 'rgba(255, 255, 255, 0.1)'; // 半透明灰色
        btn.style.color = '#FFFFFF';
        btn.style.border = 'none';
        btn.style.borderRadius = '50%'; // 变成圆形
        btn.style.display = 'flex';
        btn.style.alignItems = 'center';
        btn.style.justifyContent = 'center';
        btn.style.cursor = 'pointer';
        btn.style.transition = 'background-color 0.2s';
        btn.style.fontFamily = 'Roboto, Arial, sans-serif';
        btn.style.fontWeight = '500'; // 适配 YouTube 按钮字重
        btn.style.fontSize = '12px'; // 缩小字体，适应圆形按钮
        btn.style.margin = '0 4px'; // 适应布局

        btn.addEventListener('mouseover', () => {
            btn.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
        });

        // 按钮点击事件：复制转换后的链接
        btn.onclick = function() {
            let currentUrl = window.location.href;
            let convertedUrl = currentUrl.replace('/shorts/', '/watch?v=');
            navigator.clipboard.writeText(convertedUrl).then(() => {
                alert('Copied: ' + convertedUrl);
            });
        };

        // 插入到点赞按钮上方
        actionBar.insertBefore(btn, actionBar.firstChild);
    }

    // 监听页面变化，确保按钮在 YouTube 动态加载后仍然可用
    const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            if (mutation.addedNodes.length) {
                addCopyButton();
            }
        }
    });

    // 监听 `#actions` 父容器，而不是整个 `document.body`，提高性能
    const targetNode = document.querySelector('ytd-reel-video-renderer');
    if (targetNode) {
        observer.observe(targetNode, { childList: true, subtree: true });
    } else {
        observer.observe(document.body, { childList: true, subtree: true });
    }

    // 初次加载时执行
    addCopyButton();
})();
