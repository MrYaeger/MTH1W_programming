/*
 * py-worker.js - Python for index.html, running off the page in a web worker.
 *
 * Python here is Pyodide: the real Python, built to run inside a browser. It runs
 * in a worker so that a program which never ends can't freeze the page; if one
 * gets past harness.py's own time limit, index.html ends this worker and starts
 * a new one.
 *
 * The page sends:
 *   { cmd: "init", pyodideUrl }            start Python and load the tasks
 *   { cmd: "run", id, code, inputs, seed } the Run button
 *   { cmd: "check", id, key, code }        run one task's tests
 * and gets back:
 *   { type: "ready", python, tasks, problems }   after init
 *   { type: "failed", message }                  if Python couldn't start
 *   { type: "done", id, result }                 or { type: "done", id, crash }
 *
 * All the Python is in harness.py; the tasks are the files tasks/manifest.json lists.
 */
var harness = null;

function getText(url) {
  return fetch(url, { cache: "no-cache" }).then(function (r) {
    if (!r.ok) throw new Error(url + " (HTTP " + r.status + ")");
    return r.text();
  });
}

function start(pyodideUrl) {
  var py, problems = [];
  return import(pyodideUrl + "pyodide.mjs").then(function (mod) {
    return mod.loadPyodide({ indexURL: pyodideUrl });
  }).then(function (loaded) {
    py = loaded;
    return getText("harness.py");
  }).then(function (code) {
    py.runPython(code);
    return getText("tasks/manifest.json");
  }).then(function (text) {
    var files = JSON.parse(text);
    return Promise.all(files.map(function (file) {
      return getText("tasks/" + file).catch(function (e) { problems.push(e.message); return null; });
    })).then(function (sources) {
      var load = py.globals.get("load_task_file");
      files.forEach(function (file, i) {
        if (sources[i] === null) return;
        var problem = load(file, sources[i]);
        if (problem) problems.push(problem);
      });
    });
  }).then(function () {
    harness = { run: py.globals.get("run_json"), check: py.globals.get("check_json") };
    self.postMessage({
      type: "ready",
      python: py.runPython("import sys; sys.version.split()[0]"),
      tasks: JSON.parse(py.globals.get("catalog_json")()),
      problems: problems
    });
  });
}

self.onmessage = function (e) {
  var m = e.data;
  if (m.cmd === "init") {
    start(m.pyodideUrl).catch(function (err) {
      self.postMessage({ type: "failed", message: String(err && err.message ? err.message : err) });
    });
    return;
  }
  try {
    var text = m.cmd === "run"
      ? harness.run(m.code, JSON.stringify(m.inputs || []), m.seed)
      : harness.check(m.key, m.code);
    self.postMessage({ type: "done", id: m.id, result: JSON.parse(text) });
  } catch (err) {
    self.postMessage({ type: "done", id: m.id, crash: String(err && err.message ? err.message : err) });
  }
};
