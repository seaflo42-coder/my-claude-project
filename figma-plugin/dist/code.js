"use strict";
(() => {
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __commonJS = (cb, mod) => function __require() {
    return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
  };
  var __async = (__this, __arguments, generator) => {
    return new Promise((resolve, reject) => {
      var fulfilled = (value) => {
        try {
          step(generator.next(value));
        } catch (e) {
          reject(e);
        }
      };
      var rejected = (value) => {
        try {
          step(generator.throw(value));
        } catch (e) {
          reject(e);
        }
      };
      var step = (x) => x.done ? resolve(x.value) : Promise.resolve(x.value).then(fulfilled, rejected);
      step((generator = generator.apply(__this, __arguments)).next());
    });
  };

  // src/code.ts
  var require_code = __commonJS({
    "src/code.ts"(exports) {
      var MAPPING_KEY = "pc-mobile-mapping";
      var MODULE_PREFIX_PC = ["pc_", "PC_", "/pc_", "/PC_"];
      var MODULE_PREFIX_MOBILE = ["mobile_", "Mobile_", "mo_", "MO_", "/mobile_", "/Mobile_", "/mo_", "/MO_"];
      var CATEGORY_KEYWORDS = {
        "usp": "USP",
        "info": "\uAE30\uBCF8\uC815\uBCF4",
        "\uAE30\uBCF8\uC815\uBCF4": "\uAE30\uBCF8\uC815\uBCF4",
        "nav": "\uB124\uBE44\uAC8C\uC774\uC158",
        "\uB124\uBE44\uAC8C\uC774\uC158": "\uB124\uBE44\uAC8C\uC774\uC158",
        "schedule": "\uAD50\uC721\uC77C\uC815",
        "\uAD50\uC721\uC77C\uC815": "\uAD50\uC721\uC77C\uC815",
        "\uC77C\uC815": "\uAD50\uC721\uC77C\uC815",
        "pre": "\uC0AC\uC804\uC124\uBA85\uD68C",
        "\uC0AC\uC804\uC124\uBA85\uD68C": "\uC0AC\uC804\uC124\uBA85\uD68C",
        "\uC124\uBA85\uD68C": "\uC0AC\uC804\uC124\uBA85\uD68C",
        "header": "\uD5E4\uB354",
        "footer": "\uD478\uD130",
        "benefit": "\uD61C\uD0DD",
        "review": "\uD6C4\uAE30",
        "faq": "FAQ",
        "cta": "CTA",
        "price": "\uAC00\uACA9",
        "\uAC00\uACA9": "\uAC00\uACA9",
        "curriculum": "\uCEE4\uB9AC\uD058\uB7FC",
        "\uCEE4\uB9AC\uD058\uB7FC": "\uCEE4\uB9AC\uD058\uB7FC"
      };
      figma.showUI(__html__, {
        width: 360,
        height: 580,
        themeColors: true
      });
      function loadMapping() {
        return __async(this, null, function* () {
          const stored = figma.root.getPluginData(MAPPING_KEY);
          if (stored) {
            try {
              return JSON.parse(stored);
            } catch (e) {
              return {};
            }
          }
          return {};
        });
      }
      function saveMapping(mapping) {
        return __async(this, null, function* () {
          figma.root.setPluginData(MAPPING_KEY, JSON.stringify(mapping));
        });
      }
      function getModuleType(name) {
        const lowerName = name.toLowerCase();
        for (const prefix of MODULE_PREFIX_PC) {
          if (lowerName.includes(prefix.toLowerCase())) {
            return "pc";
          }
        }
        for (const prefix of MODULE_PREFIX_MOBILE) {
          if (lowerName.includes(prefix.toLowerCase())) {
            return "mobile";
          }
        }
        return null;
      }
      function extractCategory(name) {
        const lowerName = name.toLowerCase();
        for (const [keyword, category] of Object.entries(CATEGORY_KEYWORDS)) {
          if (lowerName.includes(keyword.toLowerCase())) {
            return category;
          }
        }
        const typeMatch = name.match(/type\d+/i);
        if (typeMatch) {
          return typeMatch[0];
        }
        return "\uAE30\uD0C0";
      }
      function getBaseName(name) {
        let baseName = name;
        const allPrefixes = [...MODULE_PREFIX_PC, ...MODULE_PREFIX_MOBILE];
        for (const prefix of allPrefixes) {
          const regex = new RegExp(prefix.replace("/", "\\/"), "gi");
          baseName = baseName.replace(regex, "");
        }
        return baseName.trim();
      }
      function scanModules() {
        const modules = [];
        const localComponents = figma.root.findAll(
          (node) => node.type === "COMPONENT" || node.type === "COMPONENT_SET"
        );
        for (const node of localComponents) {
          const moduleType = getModuleType(node.name);
          if (moduleType) {
            modules.push({
              id: node.id,
              name: node.name,
              type: moduleType,
              category: extractCategory(node.name),
              nodeId: node.id
            });
          }
        }
        modules.sort((a, b) => a.name.localeCompare(b.name, "ko"));
        return modules;
      }
      function autoCreateMapping(modules) {
        const mapping = {};
        const pcModules = modules.filter((m) => m.type === "pc");
        const mobileModules = modules.filter((m) => m.type === "mobile");
        for (const pc of pcModules) {
          const pcBaseName = getBaseName(pc.name).toLowerCase();
          let bestMatch = null;
          let bestScore = 0;
          for (const mobile of mobileModules) {
            const mobileBaseName = getBaseName(mobile.name).toLowerCase();
            if (pcBaseName === mobileBaseName) {
              bestMatch = mobile;
              break;
            }
            let score = 0;
            if (pc.category === mobile.category) {
              score += 50;
            }
            const pcWords = pcBaseName.split(/[_\-\s\/]+/);
            const mobileWords = mobileBaseName.split(/[_\-\s\/]+/);
            for (const word of pcWords) {
              if (word.length > 2 && mobileWords.includes(word)) {
                score += 10;
              }
            }
            if (score > bestScore) {
              bestScore = score;
              bestMatch = mobile;
            }
          }
          if (bestMatch) {
            mapping[pc.id] = bestMatch.id;
          }
        }
        return mapping;
      }
      function createInstance(componentId, position) {
        const component = figma.getNodeById(componentId);
        if (!component) {
          return null;
        }
        let instance;
        if (component.type === "COMPONENT") {
          instance = component.createInstance();
        } else if (component.type === "COMPONENT_SET") {
          const defaultVariant = component.defaultVariant || component.children[0];
          if (defaultVariant && defaultVariant.type === "COMPONENT") {
            instance = defaultVariant.createInstance();
          } else {
            return null;
          }
        } else {
          return null;
        }
        instance.x = position.x;
        instance.y = position.y;
        return instance;
      }
      function generatePage(pageName, moduleIds, generatePC, generateMobile) {
        return __async(this, null, function* () {
          const mapping = yield loadMapping();
          const newPage = figma.createPage();
          newPage.name = pageName;
          let pcFrame = null;
          let mobileFrame = null;
          const PC_WIDTH = 1920;
          const MOBILE_WIDTH = 750;
          const SPACING = 100;
          if (generatePC) {
            pcFrame = figma.createFrame();
            pcFrame.name = `${pageName} - PC`;
            pcFrame.resize(PC_WIDTH, 100);
            pcFrame.x = 0;
            pcFrame.y = 0;
            pcFrame.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
            pcFrame.layoutMode = "VERTICAL";
            pcFrame.primaryAxisSizingMode = "AUTO";
            pcFrame.counterAxisSizingMode = "FIXED";
            newPage.appendChild(pcFrame);
          }
          if (generateMobile) {
            mobileFrame = figma.createFrame();
            mobileFrame.name = `${pageName} - Mobile`;
            mobileFrame.resize(MOBILE_WIDTH, 100);
            mobileFrame.x = pcFrame ? PC_WIDTH + SPACING : 0;
            mobileFrame.y = 0;
            mobileFrame.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
            mobileFrame.layoutMode = "VERTICAL";
            mobileFrame.primaryAxisSizingMode = "AUTO";
            mobileFrame.counterAxisSizingMode = "FIXED";
            newPage.appendChild(mobileFrame);
          }
          for (const moduleId of moduleIds) {
            if (pcFrame) {
              const pcInstance = createInstance(moduleId, { x: 0, y: 0 });
              if (pcInstance) {
                pcFrame.appendChild(pcInstance);
                pcInstance.layoutSizingHorizontal = "FILL";
              }
            }
            if (mobileFrame && mapping[moduleId]) {
              const mobileInstance = createInstance(mapping[moduleId], { x: 0, y: 0 });
              if (mobileInstance) {
                mobileFrame.appendChild(mobileInstance);
                mobileInstance.layoutSizingHorizontal = "FILL";
              }
            }
          }
          figma.currentPage = newPage;
          const allNodes = newPage.children;
          if (allNodes.length > 0) {
            figma.viewport.scrollAndZoomIntoView(allNodes);
          }
        });
      }
      function findTextNodes(node) {
        const textNodes = [];
        if (node.type === "TEXT") {
          textNodes.push(node);
        } else if ("children" in node) {
          for (const child of node.children) {
            textNodes.push(...findTextNodes(child));
          }
        }
        return textNodes;
      }
      function findImageNodes(node) {
        const imageNodes = [];
        if ("fills" in node && Array.isArray(node.fills)) {
          const hasImage = node.fills.some((fill) => fill.type === "IMAGE");
          if (hasImage) {
            imageNodes.push(node);
          }
        }
        if ("children" in node) {
          for (const child of node.children) {
            imageNodes.push(...findImageNodes(child));
          }
        }
        return imageNodes;
      }
      function syncContent(sourceNode, targetNode, options) {
        return __async(this, null, function* () {
          let syncCount = 0;
          if (options.syncText) {
            const sourceTexts = findTextNodes(sourceNode);
            const targetTexts = findTextNodes(targetNode);
            for (const sourceText of sourceTexts) {
              const matchingTarget = targetTexts.find(
                (t) => t.name === sourceText.name || getBaseName(t.name) === getBaseName(sourceText.name)
              );
              if (matchingTarget) {
                const fontName = sourceText.fontName;
                if (fontName !== figma.mixed) {
                  yield figma.loadFontAsync(fontName);
                }
                const targetFontName = matchingTarget.fontName;
                if (targetFontName !== figma.mixed) {
                  yield figma.loadFontAsync(targetFontName);
                }
                matchingTarget.characters = sourceText.characters;
                syncCount++;
              }
            }
          }
          if (options.syncImage) {
            const sourceImages = findImageNodes(sourceNode);
            const targetImages = findImageNodes(targetNode);
            for (const sourceImg of sourceImages) {
              const matchingTarget = targetImages.find(
                (t) => t.name === sourceImg.name || getBaseName(t.name) === getBaseName(sourceImg.name)
              );
              if (matchingTarget && "fills" in sourceImg && "fills" in matchingTarget) {
                const sourceFills = sourceImg.fills;
                const imageFill = sourceFills.find((fill) => fill.type === "IMAGE");
                if (imageFill) {
                  matchingTarget.fills = [imageFill];
                  syncCount++;
                }
              }
            }
          }
          if (options.syncStyle) {
            if ("fills" in sourceNode && "fills" in targetNode && !options.syncImage) {
              targetNode.fills = sourceNode.fills;
              syncCount++;
            }
            if ("effects" in sourceNode && "effects" in targetNode) {
              targetNode.effects = sourceNode.effects;
              syncCount++;
            }
          }
          return syncCount;
        });
      }
      function findCorrespondingNode(node, mapping) {
        return __async(this, null, function* () {
          var _a;
          let current = node;
          let sourceComponent = null;
          while (current) {
            if (current.type === "COMPONENT" || current.type === "INSTANCE") {
              sourceComponent = current;
              break;
            }
            current = current.parent;
          }
          if (!sourceComponent) {
            return null;
          }
          let targetComponentId = null;
          const sourceId = sourceComponent.type === "INSTANCE" ? ((_a = sourceComponent.mainComponent) == null ? void 0 : _a.id) || "" : sourceComponent.id;
          if (mapping[sourceId]) {
            targetComponentId = mapping[sourceId];
          } else {
            for (const [pcId, mobileId] of Object.entries(mapping)) {
              if (mobileId === sourceId) {
                targetComponentId = pcId;
                break;
              }
            }
          }
          if (!targetComponentId) {
            return null;
          }
          const targetComponent = figma.getNodeById(targetComponentId);
          if (!targetComponent) {
            return null;
          }
          const nodePath = getNodePath(node, sourceComponent);
          return findNodeByPath(targetComponent, nodePath);
        });
      }
      function getNodePath(node, ancestor) {
        const path = [];
        let current = node;
        while (current && current !== ancestor) {
          path.unshift(current.name);
          current = current.parent;
        }
        return path;
      }
      function findNodeByPath(root, path) {
        if (path.length === 0) {
          return root;
        }
        if (!("children" in root)) {
          return null;
        }
        const [first, ...rest] = path;
        const child = root.children.find((c) => c.name === first || getBaseName(c.name) === getBaseName(first));
        if (!child) {
          return null;
        }
        if (rest.length === 0) {
          return child;
        }
        return findNodeByPath(child, rest);
      }
      function syncAllModules(options, direction) {
        return __async(this, null, function* () {
          const mapping = yield loadMapping();
          let totalSyncCount = 0;
          const instances = figma.currentPage.findAll((n) => n.type === "INSTANCE");
          for (const instance of instances) {
            const mainComponent = instance.mainComponent;
            if (!mainComponent)
              continue;
            const componentId = mainComponent.id;
            let targetId = null;
            if (direction === "pc-to-mobile" && mapping[componentId]) {
              targetId = mapping[componentId];
            } else if (direction === "mobile-to-pc") {
              for (const [pcId, mobileId] of Object.entries(mapping)) {
                if (mobileId === componentId) {
                  targetId = pcId;
                  break;
                }
              }
            }
            if (!targetId)
              continue;
            const targetInstances = instances.filter((i) => {
              var _a;
              return ((_a = i.mainComponent) == null ? void 0 : _a.id) === targetId;
            });
            for (const targetInstance of targetInstances) {
              const count = yield syncContent(instance, targetInstance, options);
              totalSyncCount += count;
            }
          }
          return totalSyncCount;
        });
      }
      figma.on("selectionchange", () => {
        const selection = figma.currentPage.selection.map((node) => ({
          id: node.id,
          name: node.name,
          type: node.type
        }));
        figma.ui.postMessage({
          type: "selection-change",
          selection
        });
      });
      figma.ui.onmessage = (msg) => __async(exports, null, function* () {
        try {
          switch (msg.type) {
            case "scan-modules": {
              const modules = scanModules();
              const existingMapping = yield loadMapping();
              let mapping = existingMapping;
              if (Object.keys(existingMapping).length === 0) {
                mapping = autoCreateMapping(modules);
                yield saveMapping(mapping);
              }
              figma.ui.postMessage({
                type: "scan-result",
                modules
              });
              figma.ui.postMessage({
                type: "mapping-loaded",
                mapping
              });
              figma.notify(`\u2705 ${modules.length}\uAC1C \uBAA8\uB4C8 \uC2A4\uCE94 \uC644\uB8CC`);
              break;
            }
            case "save-mapping": {
              yield saveMapping(msg.mapping);
              figma.notify("\u2705 \uB9E4\uD551 \uC800\uC7A5 \uC644\uB8CC");
              break;
            }
            case "generate-page": {
              const { pageName, generatePC, generateMobile, modules } = msg;
              const moduleIds = modules.map((m) => m.id);
              yield generatePage(pageName, moduleIds, generatePC, generateMobile);
              figma.notify(`\u2705 "${pageName}" \uD398\uC774\uC9C0 \uC0DD\uC131 \uC644\uB8CC`);
              break;
            }
            case "preview-page": {
              const moduleIds = msg.modules.map((m) => m.id);
              const nodes = moduleIds.map((id) => figma.getNodeById(id)).filter((n) => n !== null);
              if (nodes.length > 0) {
                figma.currentPage.selection = nodes;
                figma.viewport.scrollAndZoomIntoView(nodes);
              }
              break;
            }
            case "sync": {
              const { direction, syncText, syncImage, syncStyle } = msg;
              const options = { syncText, syncImage, syncStyle };
              const selection = figma.currentPage.selection;
              if (selection.length === 0) {
                figma.notify("\u26A0\uFE0F \uB3D9\uAE30\uD654\uD560 \uC694\uC18C\uB97C \uC120\uD0DD\uD574\uC8FC\uC138\uC694");
                return;
              }
              const mapping = yield loadMapping();
              let syncCount = 0;
              for (const node of selection) {
                const correspondingNode = yield findCorrespondingNode(node, mapping);
                if (correspondingNode) {
                  if (direction === "pc-to-mobile" || direction === "both") {
                    syncCount += yield syncContent(node, correspondingNode, options);
                  }
                  if (direction === "mobile-to-pc" || direction === "both") {
                    syncCount += yield syncContent(correspondingNode, node, options);
                  }
                }
              }
              figma.notify(`\u2705 ${syncCount}\uAC1C \uD56D\uBAA9 \uB3D9\uAE30\uD654 \uC644\uB8CC`);
              break;
            }
            case "sync-all": {
              const { syncText, syncImage, syncStyle } = msg;
              const options = { syncText, syncImage, syncStyle };
              const countPcToMobile = yield syncAllModules(options, "pc-to-mobile");
              figma.notify(`\u2705 \uC804\uCCB4 \uD398\uC774\uC9C0 \uB3D9\uAE30\uD654 \uC644\uB8CC (${countPcToMobile}\uAC1C \uD56D\uBAA9)`);
              break;
            }
          }
        } catch (error) {
          console.error(error);
          figma.notify(`\u274C \uC624\uB958: ${error instanceof Error ? error.message : "\uC54C \uC218 \uC5C6\uB294 \uC624\uB958"}`, {
            error: true
          });
        }
      });
      loadMapping().then((mapping) => {
        figma.ui.postMessage({
          type: "mapping-loaded",
          mapping
        });
      });
    }
  });
  require_code();
})();
