(function () {
  "use strict";

  var root = document.documentElement;
  var body = document.body;
  var themeStorageKey = "grx-theme";

  function $(selector, context) {
    return (context || document).querySelector(selector);
  }

  function $$(selector, context) {
    return Array.prototype.slice.call((context || document).querySelectorAll(selector));
  }

  function isEnglish() {
    return (root.lang || "").toLowerCase().indexOf("en") === 0;
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTheme();
    initLanguage();
    initSearch();
    initToc();
    initCallouts();
    initTaskMeta();
    initCodeLabels();
    initBackToTop();
    initMobileNav();
    initSearchMobile();
    initNavGroups();
  });

  function initTheme() {
    var button = $("#grx-theme-toggle");
    if (!button) return;

    function apply(theme) {
      root.setAttribute("data-theme", theme);
      var label =
        theme === "dark"
          ? isEnglish()
            ? "Switch to light mode"
            : "切换到浅色模式"
          : isEnglish()
            ? "Switch to dark mode"
            : "切换到深色模式";
      button.setAttribute("aria-label", label);
      button.setAttribute("title", label);
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) meta.setAttribute("content", theme === "dark" ? "#0b1120" : "#ffffff");
    }

    var theme = root.getAttribute("data-theme");
    if (theme !== "dark" && theme !== "light") {
      theme =
        window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
          ? "dark"
          : "light";
    }
    apply(theme);

    button.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      apply(next);
      try {
        window.localStorage.setItem(themeStorageKey, next);
      } catch (error) {
        /* localStorage may be unavailable */
      }
    });
  }

  function initLanguage() {
    var wrap = $("#grx-lang");
    var button = $("#grx-lang-btn");
    var zhLink = $("#lang-zh-btn");
    var enLink = $("#lang-en-btn");
    if (!wrap || !button || !zhLink || !enLink) return;

    var path = window.location.pathname;
    var isEnPage = path.indexOf("/docs/en") !== -1;
    var cut = path.indexOf("/docs/");
    var demoCut = path.indexOf("/demo/");
    var siteRoot;
    if (cut !== -1) {
      siteRoot = path.slice(0, cut) + "/";
    } else if (demoCut !== -1) {
      siteRoot = path.slice(0, demoCut) + "/";
    } else {
      siteRoot = path.replace(/[^/]*$/, "");
    }
    var zhPath;
    var enPath;

    if (isEnPage) {
      enPath = path;
      zhPath = /\/docs\/en\/?([^/]+\.html)?$/.test(path)
        ? siteRoot
        : path.replace("/docs/en", "/docs");
    } else {
      zhPath = path;
      enPath = cut === -1 ? siteRoot + "docs/en/" : path.replace("/docs/", "/docs/en/");
    }

    zhLink.href = zhPath;
    enLink.href = enPath;
    zhLink.classList.toggle("is-active", !isEnPage);
    enLink.classList.toggle("is-active", isEnPage);

    var label = $("#grx-lang-label");
    if (label) label.textContent = isEnPage ? "English" : "中文";

    button.addEventListener("click", function (event) {
      event.stopPropagation();
      var open = wrap.classList.toggle("is-open");
      button.setAttribute("aria-expanded", open ? "true" : "false");
    });

    document.addEventListener("click", function (event) {
      if (!wrap.contains(event.target)) {
        wrap.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        wrap.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
      }
    });
  }

  function initSearch() {
    var input = $("#search-input");
    var search = $("#grx-search");
    if (!input) return;

    document.addEventListener("keydown", function (event) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        input.focus();
        input.select();
      }
    });

    document.addEventListener("click", function (event) {
      if (!search || search.contains(event.target)) return;
      if (input.value.trim() !== "") {
        input.value = "";
        input.dispatchEvent(new Event("input", { bubbles: true }));
        input.blur();
        document.documentElement.classList.remove("search-active");
      }
    });
  }

  function initSearchMobile() {
    var search = $("#grx-search");
    if (!search) return;

    search.addEventListener("click", function (event) {
      if (!window.matchMedia("(max-width: 40rem)").matches) return;
      if (search.classList.contains("is-open")) return;
      event.preventDefault();
      search.classList.add("is-open");
      var input = $("#search-input");
      if (input) input.focus();
    });

    document.addEventListener("click", function (event) {
      if (!search.contains(event.target)) search.classList.remove("is-open");
    });
  }

  function initToc() {
    var toc = $("#grx-toc");
    var nav = $("#grx-toc-nav");
    var content = $(".main-content");
    if (!toc || !nav || !content) return;

    var headings = $$("h2, h3", content).filter(function (heading) {
      return heading.id && !heading.closest(".grx-steps") && !heading.closest(".grx-callout");
    });

    if (headings.length < 2) {
      toc.hidden = true;
      return;
    }

    var links = [];
    headings.forEach(function (heading) {
      var link = document.createElement("a");
      link.className = "grx-toc__link level-" + heading.tagName.slice(1).toLowerCase();
      link.href = "#" + heading.id;
      link.textContent = (heading.textContent || "").replace(/\u200b/g, "").trim();
      nav.appendChild(link);
      links.push({ link: link, heading: heading });
    });

    function setActive(id) {
      links.forEach(function (item) {
        item.link.classList.toggle("is-active", item.heading.id === id);
      });
    }

    function updateActive() {
      var current = headings[0];
      headings.forEach(function (heading) {
        if (heading.getBoundingClientRect().top <= 140) current = heading;
      });
      if (current) setActive(current.id);
    }

    window.addEventListener("scroll", updateActive, { passive: true });
    updateActive();
  }

  function initCallouts() {
    $$(".main-content blockquote").forEach(function (quote) {
      if (quote.classList.contains("grx-callout") || quote.closest(".grx-callout")) return;
      var text = quote.textContent || "";
      var level = "info";
      if (/危险|严禁|切勿|瘫软|跌落|触电|Danger/i.test(text)) {
        level = "danger";
      } else if (
        /注意|警告|warning|已废弃|deprecated|版本变更|version change|不兼容|breaking/i.test(
          text
        )
      ) {
        level = "warn";
      }

      quote.classList.add("grx-callout", "grx-callout--" + level);

      var icon = document.createElement("span");
      icon.className = "grx-callout__icon";
      icon.innerHTML =
        '<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#' +
        (level === "info" ? "grx-info" : "grx-warning") +
        '"></use></svg>';

      var bodyNode = document.createElement("div");
      bodyNode.className = "grx-callout__body";
      while (quote.firstChild) bodyNode.appendChild(quote.firstChild);

      stripLeadingEmoji(bodyNode);

      quote.appendChild(icon);
      quote.appendChild(bodyNode);
    });
  }

  function stripLeadingEmoji(node) {
    for (var index = 0; index < node.childNodes.length; index += 1) {
      var child = node.childNodes[index];
      if (child.nodeType === 3) {
        var text = child.nodeValue;
        var replaced = text.replace(/^\s*(?:⚠️|⚠|ℹ️|ℹ)\s*/, "");
        if (replaced !== text) {
          child.nodeValue = replaced;
          return true;
        }
        if (replaced.trim() !== "") return true;
      } else if (child.nodeType === 1 && stripLeadingEmoji(child)) {
        return true;
      }
    }
    return false;
  }

  function initTaskMeta() {
    if (!body.classList.contains("grx-task-page")) return;
    var content = $(".main-content");
    if (!content) return;

    var metaParagraph = null;
    var metaText = "";
    $$("p", content).some(function (paragraph) {
      var text = paragraph.textContent || "";
      if (/任务值\s*[（(]?\s*TID|Task (?:value|ID)\s*\(TID\)/i.test(text)) {
        metaParagraph = paragraph;
        metaText = text;
        return true;
      }
      return false;
    });

    if (!metaParagraph) return;

    var tidMatch =
      metaText.match(/TID\s*[)）]?\s*[：:]\s*\**\s*(\d{2,5})/i) ||
      metaText.match(/(\d{3,5})/);
    if (!tidMatch) return;

    var noteMatch = metaText.match(
      /[（(]\s*([^）)]*(?:此前|previously|之前)[^）)]*)[）)]/i
    );

    var row = document.createElement("div");
    row.className = "grx-chip-row";

    function addChip(text, className) {
      var chip = document.createElement("span");
      chip.className = "grx-chip" + (className ? " " + className : "");
      chip.textContent = text;
      row.appendChild(chip);
    }

    addChip("TID " + tidMatch[1], "grx-chip--mono");
    addChip(isEnglish() ? "Robot M4L" : "适用机型 M4L", "grx-chip--brand");
    if (noteMatch) {
      var note = noteMatch[1].trim();
      var tidChange = note.match(/^(v[\d.]+)\s*起[；;]?\s*此前为\s*(\d+)$/);
      if (tidChange) note = tidChange[1] + " 前为 " + tidChange[2];
      addChip(note, "grx-chip--warn");
    }

    var heading = content.querySelector("h1");
    if (heading) {
      heading.insertAdjacentElement("afterend", row);
    } else {
      metaParagraph.parentNode.insertBefore(row, metaParagraph);
    }
    metaParagraph.classList.add("grx-source-meta");
  }

  function initCodeLabels() {
    var labels = {
      python: "Python",
      py: "Python",
      bash: "Bash",
      shell: "Shell",
      sh: "Shell",
      zsh: "Shell",
      yaml: "YAML",
      yml: "YAML",
      json: "JSON",
      cpp: "C++",
      cxx: "C++",
      c: "C",
      js: "JavaScript",
      javascript: "JavaScript",
      ts: "TypeScript",
      typescript: "TypeScript",
      powershell: "PowerShell",
      ps1: "PowerShell",
      bat: "Batch",
      cmd: "Batch",
      html: "HTML",
      css: "CSS",
      scss: "SCSS",
      md: "Markdown",
      markdown: "Markdown",
      text: "Text",
      plaintext: "Text",
      ini: "INI",
      toml: "TOML",
      xml: "XML",
      sql: "SQL",
      makefile: "Makefile",
      dockerfile: "Dockerfile"
    };

    $$("div.highlighter-rouge, figure.highlight").forEach(function (block) {
      var code = block.querySelector("code");
      var className = (code && code.className) || block.className || "";
      var match = className.match(/language-([\w+-]+)/);
      if (!match) return;
      var language = match[1].toLowerCase();
      block.setAttribute("data-lang", labels[language] || language.toUpperCase());
    });
  }

  function initBackToTop() {
    var button = $("#grx-top-btn");
    if (!button) return;

    function update() {
      button.classList.toggle("is-visible", window.scrollY > 480);
    }

    window.addEventListener("scroll", update, { passive: true });
    update();

    button.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  function initNavGroups() {
    document.addEventListener("click", function (event) {
      var label = event.target.closest(".grx-nav-group-label");
      if (!label) return;
      var item = label.closest(".nav-list-item");
      if (!item) return;
      var toggle = item.querySelector(":scope > .nav-list-expander");
      if (toggle) toggle.click();
    });
  }

  function initMobileNav() {
    var menu = $("#menu-button");
    var nav = $("#site-nav");
    if (!menu || !nav) return;

    function close() {
      body.classList.remove("grx-nav-open");
      nav.classList.remove("nav-open");
      menu.classList.remove("nav-open");
      menu.setAttribute("aria-expanded", "false");
    }

    menu.addEventListener("click", function () {
      window.setTimeout(function () {
        body.classList.toggle("grx-nav-open", nav.classList.contains("nav-open"));
      }, 0);
    });

    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) close();
    });

    document.addEventListener("click", function (event) {
      if (!body.classList.contains("grx-nav-open")) return;
      var sidebar = $("#grx-sidebar");
      if (sidebar && !sidebar.contains(event.target) && !menu.contains(event.target)) close();
    });
  }
})();
