// More info about initialization & config:
// - https://revealjs.com/initialization/
// - https://revealjs.com/config/

const isLocalServer =
  window.location.hostname.indexOf("localhost") !== -1 ||
  window.location.hostname.indexOf("127.0.0.1") !== -1;

Reveal.initialize({
  hash: true,
  // do not change url for each fragment that is visible
  fragmentInURL: false,

  // do not use fragments at all in 'public' version
  fragments: false,

  controls: true,
  progress: true,
  history: true,
  center: true,
  slideNumber: true,
  transition: 'none', // none/fade/slide/convex/concave/zoom


  // i need all space i can get
  width: 1100,
  // height: 1200,

  // there's a bug with Firefox that does not show
  // the cursor again after is has been hidden, so disable
  hideInactiveCursor: false,

  // Learn about plugins: https://revealjs.com/plugins/
  plugins: [RevealMarkdown, RevealHighlight, RevealNotes],
}).then(() => {
  if (isLocalServer) {
    // only applies to presentation version

    // As a presenter I don't need controls but fragments
    Reveal.configure({ controls: false, fragments: true });

    // every 'li' should become a fragment
    document.querySelectorAll(".fragments li").forEach((n) => n.classList.add("fragment"));

    // when using code blocks with markdown like this:
    //  ```java fragment
    //  the <code> elements gets the "fragment" class, but it needs
    //  to be on its parent <pre> element
    document.querySelectorAll("code.fragment").forEach((n) => {
      n.classList.remove("fragment");
      n.parentNode.classList.add("fragment");
    });
    // surround all pre.fragment blocks with a 'div.fragment'
    // (somehow this seems to work better with code fragments)
    document.querySelectorAll("pre.fragment").forEach((n) => {
      n.classList.remove("fragment");
      const div = document.createElement("div");
      div.classList.add("fragment");
      n.parentNode.insertBefore(div, n);
      div.appendChild(n);
    });

    // li having a code inside, should not have a bullet point (see also styles.css)
    document.querySelectorAll("li > pre.code-wrapper").forEach((n) => {
      n.parentNode.classList.add("no-icon");
    });
  } else {
    // public version

    // remove presenter "demo" marks (children of demo)
    document.querySelectorAll(".demo .demo").forEach((n) => n.remove());
    // remove todos and other local stuff
    document.querySelectorAll(".todo").forEach((n) => n.remove());
    document.querySelectorAll(".local").forEach((n) => n.remove());
    document.querySelectorAll(".hide").forEach((n) => n.remove());
    document.querySelectorAll(".preparation").forEach((n) => n.remove());
  }

  // Changes for both public and presenter version

  // open all externals link in new tab
  document.querySelectorAll('a:not([href^="#"])').forEach((i) => {
    i.setAttribute("target", "_blank");
  });

  // make all code editable
  document.querySelectorAll("pre code").forEach((n) => {
    n.setAttribute("contenteditable", "true");
  });

  // small lists
  document.querySelectorAll("li.small").forEach((n) => {
    n.classList.remove("small");
    n.parentNode.classList.add("small");
    n.remove();
  });
});
