(() => {
    const toc = document.getElementById("SidebarTableOfContents");
    if (!toc) return;

    const sections = Array.from(toc.querySelectorAll('a[href^="#"]'), link => ({
        link,
        heading: document.getElementById(decodeURIComponent(link.hash.slice(1))),
    })).filter(({ heading }) => heading);

    let active;
    let pending = false;
    function update() {
        pending = false;
        let current;
        const readingLine = Math.min(120, window.innerHeight * 0.25);
        for (const { heading, link } of sections) {
            if (heading.getBoundingClientRect().top > readingLine) break;
            current = link;
        }
        const pageHeight = document.documentElement.scrollHeight;
        if (pageHeight > window.innerHeight && window.scrollY + window.innerHeight >= pageHeight - 2) {
            current = sections.at(-1)?.link;
        }
        if (current === active) return;
        active?.removeAttribute("aria-current");
        current?.setAttribute("aria-current", "location");
        active = current;
    }

    function schedule() {
        if (pending) return;
        pending = true;
        requestAnimationFrame(update);
    }
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    window.addEventListener("load", schedule);
    schedule();
})();
