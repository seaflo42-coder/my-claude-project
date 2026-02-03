// PC↔모바일 상세페이지 자동화 Figma Plugin

// 타입 정의
interface ModuleInfo {
  id: string;
  name: string;
  type: 'pc' | 'mobile';
  category: string;
  nodeId: string;
}

interface ModuleMapping {
  [pcId: string]: string; // pcId -> mobileId
}

interface SyncOptions {
  syncText: boolean;
  syncImage: boolean;
  syncStyle: boolean;
}

// 플러그인 데이터 키
const MAPPING_KEY = 'pc-mobile-mapping';
const MODULE_PREFIX_PC = ['pc_', 'PC_', '/pc_', '/PC_'];
const MODULE_PREFIX_MOBILE = ['mobile_', 'Mobile_', 'mo_', 'MO_', '/mobile_', '/Mobile_', '/mo_', '/MO_'];

// 카테고리 키워드 매핑
const CATEGORY_KEYWORDS: { [key: string]: string } = {
  'usp': 'USP',
  'info': '기본정보',
  '기본정보': '기본정보',
  'nav': '네비게이션',
  '네비게이션': '네비게이션',
  'schedule': '교육일정',
  '교육일정': '교육일정',
  '일정': '교육일정',
  'pre': '사전설명회',
  '사전설명회': '사전설명회',
  '설명회': '사전설명회',
  'header': '헤더',
  'footer': '푸터',
  'benefit': '혜택',
  'review': '후기',
  'faq': 'FAQ',
  'cta': 'CTA',
  'price': '가격',
  '가격': '가격',
  'curriculum': '커리큘럼',
  '커리큘럼': '커리큘럼',
};

// UI 표시
figma.showUI(__html__, {
  width: 360,
  height: 580,
  themeColors: true
});

// 저장된 매핑 로드
async function loadMapping(): Promise<ModuleMapping> {
  const stored = figma.root.getPluginData(MAPPING_KEY);
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      return {};
    }
  }
  return {};
}

// 매핑 저장
async function saveMapping(mapping: ModuleMapping): Promise<void> {
  figma.root.setPluginData(MAPPING_KEY, JSON.stringify(mapping));
}

// 모듈 타입 판별
function getModuleType(name: string): 'pc' | 'mobile' | null {
  const lowerName = name.toLowerCase();

  for (const prefix of MODULE_PREFIX_PC) {
    if (lowerName.includes(prefix.toLowerCase())) {
      return 'pc';
    }
  }

  for (const prefix of MODULE_PREFIX_MOBILE) {
    if (lowerName.includes(prefix.toLowerCase())) {
      return 'mobile';
    }
  }

  return null;
}

// 카테고리 추출
function extractCategory(name: string): string {
  const lowerName = name.toLowerCase();

  for (const [keyword, category] of Object.entries(CATEGORY_KEYWORDS)) {
    if (lowerName.includes(keyword.toLowerCase())) {
      return category;
    }
  }

  // 타입 번호 추출 (예: type1, type2)
  const typeMatch = name.match(/type\d+/i);
  if (typeMatch) {
    return typeMatch[0];
  }

  return '기타';
}

// 모듈 이름에서 기본 이름 추출 (PC/Mobile 프리픽스 제거)
function getBaseName(name: string): string {
  let baseName = name;

  // 프리픽스 제거
  const allPrefixes = [...MODULE_PREFIX_PC, ...MODULE_PREFIX_MOBILE];
  for (const prefix of allPrefixes) {
    const regex = new RegExp(prefix.replace('/', '\\/'), 'gi');
    baseName = baseName.replace(regex, '');
  }

  return baseName.trim();
}

// 컴포넌트/컴포넌트 세트 스캔
function scanModules(): ModuleInfo[] {
  const modules: ModuleInfo[] = [];
  const localComponents = figma.root.findAll(node =>
    node.type === 'COMPONENT' || node.type === 'COMPONENT_SET'
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

  // 이름으로 정렬
  modules.sort((a, b) => a.name.localeCompare(b.name, 'ko'));

  return modules;
}

// 자동 매핑 생성 (이름 기반)
function autoCreateMapping(modules: ModuleInfo[]): ModuleMapping {
  const mapping: ModuleMapping = {};
  const pcModules = modules.filter(m => m.type === 'pc');
  const mobileModules = modules.filter(m => m.type === 'mobile');

  for (const pc of pcModules) {
    const pcBaseName = getBaseName(pc.name).toLowerCase();

    // 가장 유사한 모바일 모듈 찾기
    let bestMatch: ModuleInfo | null = null;
    let bestScore = 0;

    for (const mobile of mobileModules) {
      const mobileBaseName = getBaseName(mobile.name).toLowerCase();

      // 정확히 일치하는 경우
      if (pcBaseName === mobileBaseName) {
        bestMatch = mobile;
        break;
      }

      // 카테고리가 같은 경우 가산점
      let score = 0;
      if (pc.category === mobile.category) {
        score += 50;
      }

      // 이름에 공통 키워드가 있는 경우
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

// 인스턴스 생성
function createInstance(componentId: string, position: { x: number; y: number }): InstanceNode | null {
  const component = figma.getNodeById(componentId);

  if (!component) {
    return null;
  }

  let instance: InstanceNode;

  if (component.type === 'COMPONENT') {
    instance = component.createInstance();
  } else if (component.type === 'COMPONENT_SET') {
    // 컴포넌트 세트의 경우 기본 variant 사용
    const defaultVariant = component.defaultVariant || component.children[0];
    if (defaultVariant && defaultVariant.type === 'COMPONENT') {
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

// 페이지 생성
async function generatePage(
  pageName: string,
  moduleIds: string[],
  generatePC: boolean,
  generateMobile: boolean
): Promise<void> {
  const mapping = await loadMapping();

  // 새 페이지 생성
  const newPage = figma.createPage();
  newPage.name = pageName;

  // PC 프레임 생성
  let pcFrame: FrameNode | null = null;
  let mobileFrame: FrameNode | null = null;

  const PC_WIDTH = 1920;
  const MOBILE_WIDTH = 750;
  const SPACING = 100;

  if (generatePC) {
    pcFrame = figma.createFrame();
    pcFrame.name = `${pageName} - PC`;
    pcFrame.resize(PC_WIDTH, 100);
    pcFrame.x = 0;
    pcFrame.y = 0;
    pcFrame.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
    pcFrame.layoutMode = 'VERTICAL';
    pcFrame.primaryAxisSizingMode = 'AUTO';
    pcFrame.counterAxisSizingMode = 'FIXED';
    newPage.appendChild(pcFrame);
  }

  if (generateMobile) {
    mobileFrame = figma.createFrame();
    mobileFrame.name = `${pageName} - Mobile`;
    mobileFrame.resize(MOBILE_WIDTH, 100);
    mobileFrame.x = (pcFrame ? PC_WIDTH + SPACING : 0);
    mobileFrame.y = 0;
    mobileFrame.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
    mobileFrame.layoutMode = 'VERTICAL';
    mobileFrame.primaryAxisSizingMode = 'AUTO';
    mobileFrame.counterAxisSizingMode = 'FIXED';
    newPage.appendChild(mobileFrame);
  }

  // 모듈 인스턴스 생성
  for (const moduleId of moduleIds) {
    // PC 모듈 추가
    if (pcFrame) {
      const pcInstance = createInstance(moduleId, { x: 0, y: 0 });
      if (pcInstance) {
        pcFrame.appendChild(pcInstance);
        pcInstance.layoutSizingHorizontal = 'FILL';
      }
    }

    // 모바일 모듈 추가
    if (mobileFrame && mapping[moduleId]) {
      const mobileInstance = createInstance(mapping[moduleId], { x: 0, y: 0 });
      if (mobileInstance) {
        mobileFrame.appendChild(mobileInstance);
        mobileInstance.layoutSizingHorizontal = 'FILL';
      }
    }
  }

  // 생성된 페이지로 이동
  figma.currentPage = newPage;

  // 뷰포트 맞춤
  const allNodes = newPage.children;
  if (allNodes.length > 0) {
    figma.viewport.scrollAndZoomIntoView(allNodes);
  }
}

// 텍스트 노드 찾기
function findTextNodes(node: SceneNode): TextNode[] {
  const textNodes: TextNode[] = [];

  if (node.type === 'TEXT') {
    textNodes.push(node);
  } else if ('children' in node) {
    for (const child of node.children) {
      textNodes.push(...findTextNodes(child as SceneNode));
    }
  }

  return textNodes;
}

// 이미지 노드 찾기 (fills에 이미지가 있는 노드)
function findImageNodes(node: SceneNode): SceneNode[] {
  const imageNodes: SceneNode[] = [];

  if ('fills' in node && Array.isArray(node.fills)) {
    const hasImage = node.fills.some((fill: Paint) => fill.type === 'IMAGE');
    if (hasImage) {
      imageNodes.push(node);
    }
  }

  if ('children' in node) {
    for (const child of node.children) {
      imageNodes.push(...findImageNodes(child as SceneNode));
    }
  }

  return imageNodes;
}

// 콘텐츠 동기화
async function syncContent(
  sourceNode: SceneNode,
  targetNode: SceneNode,
  options: SyncOptions
): Promise<number> {
  let syncCount = 0;

  // 텍스트 동기화
  if (options.syncText) {
    const sourceTexts = findTextNodes(sourceNode);
    const targetTexts = findTextNodes(targetNode);

    // 이름 기반 매칭
    for (const sourceText of sourceTexts) {
      const matchingTarget = targetTexts.find(t =>
        t.name === sourceText.name ||
        getBaseName(t.name) === getBaseName(sourceText.name)
      );

      if (matchingTarget) {
        // 폰트 로드
        const fontName = sourceText.fontName;
        if (fontName !== figma.mixed) {
          await figma.loadFontAsync(fontName);
        }

        const targetFontName = matchingTarget.fontName;
        if (targetFontName !== figma.mixed) {
          await figma.loadFontAsync(targetFontName);
        }

        // 텍스트 복사
        matchingTarget.characters = sourceText.characters;
        syncCount++;
      }
    }
  }

  // 이미지 동기화
  if (options.syncImage) {
    const sourceImages = findImageNodes(sourceNode);
    const targetImages = findImageNodes(targetNode);

    for (const sourceImg of sourceImages) {
      const matchingTarget = targetImages.find(t =>
        t.name === sourceImg.name ||
        getBaseName(t.name) === getBaseName(sourceImg.name)
      );

      if (matchingTarget && 'fills' in sourceImg && 'fills' in matchingTarget) {
        const sourceFills = sourceImg.fills as Paint[];
        const imageFill = sourceFills.find((fill: Paint) => fill.type === 'IMAGE');

        if (imageFill) {
          (matchingTarget as GeometryMixin).fills = [imageFill];
          syncCount++;
        }
      }
    }
  }

  // 스타일 동기화
  if (options.syncStyle) {
    // 기본 스타일 속성 동기화 (색상, 효과 등)
    if ('fills' in sourceNode && 'fills' in targetNode && !options.syncImage) {
      (targetNode as GeometryMixin).fills = (sourceNode as GeometryMixin).fills;
      syncCount++;
    }

    if ('effects' in sourceNode && 'effects' in targetNode) {
      (targetNode as BlendMixin).effects = (sourceNode as BlendMixin).effects;
      syncCount++;
    }
  }

  return syncCount;
}

// 선택된 노드의 대응 노드 찾기
async function findCorrespondingNode(node: SceneNode, mapping: ModuleMapping): Promise<SceneNode | null> {
  // 노드가 속한 컴포넌트/인스턴스 찾기
  let current: BaseNode | null = node;
  let sourceComponent: ComponentNode | InstanceNode | null = null;

  while (current) {
    if (current.type === 'COMPONENT' || current.type === 'INSTANCE') {
      sourceComponent = current;
      break;
    }
    current = current.parent;
  }

  if (!sourceComponent) {
    return null;
  }

  // 매핑에서 대응 컴포넌트 찾기
  let targetComponentId: string | null = null;
  const sourceId = sourceComponent.type === 'INSTANCE'
    ? (sourceComponent.mainComponent?.id || '')
    : sourceComponent.id;

  // PC -> Mobile 또는 Mobile -> PC
  if (mapping[sourceId]) {
    targetComponentId = mapping[sourceId];
  } else {
    // 역방향 매핑 확인
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

  // 대응 컴포넌트 찾기
  const targetComponent = figma.getNodeById(targetComponentId);
  if (!targetComponent) {
    return null;
  }

  // 노드 경로를 통해 대응 노드 찾기
  const nodePath = getNodePath(node, sourceComponent);

  return findNodeByPath(targetComponent as SceneNode, nodePath);
}

// 노드 경로 추출
function getNodePath(node: BaseNode, ancestor: BaseNode): string[] {
  const path: string[] = [];
  let current: BaseNode | null = node;

  while (current && current !== ancestor) {
    path.unshift(current.name);
    current = current.parent;
  }

  return path;
}

// 경로로 노드 찾기
function findNodeByPath(root: SceneNode, path: string[]): SceneNode | null {
  if (path.length === 0) {
    return root;
  }

  if (!('children' in root)) {
    return null;
  }

  const [first, ...rest] = path;
  const child = root.children.find(c => c.name === first || getBaseName(c.name) === getBaseName(first));

  if (!child) {
    return null;
  }

  if (rest.length === 0) {
    return child as SceneNode;
  }

  return findNodeByPath(child as SceneNode, rest);
}

// 전체 페이지 동기화
async function syncAllModules(options: SyncOptions, direction: 'pc-to-mobile' | 'mobile-to-pc'): Promise<number> {
  const mapping = await loadMapping();
  let totalSyncCount = 0;

  // 현재 페이지의 모든 인스턴스 찾기
  const instances = figma.currentPage.findAll(n => n.type === 'INSTANCE') as InstanceNode[];

  for (const instance of instances) {
    const mainComponent = instance.mainComponent;
    if (!mainComponent) continue;

    const componentId = mainComponent.id;
    let targetId: string | null = null;

    if (direction === 'pc-to-mobile' && mapping[componentId]) {
      targetId = mapping[componentId];
    } else if (direction === 'mobile-to-pc') {
      for (const [pcId, mobileId] of Object.entries(mapping)) {
        if (mobileId === componentId) {
          targetId = pcId;
          break;
        }
      }
    }

    if (!targetId) continue;

    // 대응 인스턴스 찾기
    const targetInstances = instances.filter(i => i.mainComponent?.id === targetId);

    for (const targetInstance of targetInstances) {
      const count = await syncContent(instance, targetInstance, options);
      totalSyncCount += count;
    }
  }

  return totalSyncCount;
}

// 선택 변경 감지
figma.on('selectionchange', () => {
  const selection = figma.currentPage.selection.map(node => ({
    id: node.id,
    name: node.name,
    type: node.type
  }));

  figma.ui.postMessage({
    type: 'selection-change',
    selection
  });
});

// 메시지 핸들러
figma.ui.onmessage = async (msg: any) => {
  try {
    switch (msg.type) {
      case 'scan-modules': {
        const modules = scanModules();
        const existingMapping = await loadMapping();

        // 기존 매핑이 없으면 자동 매핑 생성
        let mapping = existingMapping;
        if (Object.keys(existingMapping).length === 0) {
          mapping = autoCreateMapping(modules);
          await saveMapping(mapping);
        }

        figma.ui.postMessage({
          type: 'scan-result',
          modules
        });

        figma.ui.postMessage({
          type: 'mapping-loaded',
          mapping
        });

        figma.notify(`✅ ${modules.length}개 모듈 스캔 완료`);
        break;
      }

      case 'save-mapping': {
        await saveMapping(msg.mapping);
        figma.notify('✅ 매핑 저장 완료');
        break;
      }

      case 'generate-page': {
        const { pageName, generatePC, generateMobile, modules } = msg;
        const moduleIds = modules.map((m: ModuleInfo) => m.id);

        await generatePage(pageName, moduleIds, generatePC, generateMobile);
        figma.notify(`✅ "${pageName}" 페이지 생성 완료`);
        break;
      }

      case 'preview-page': {
        // 선택된 모듈 하이라이트
        const moduleIds = msg.modules.map((m: ModuleInfo) => m.id);
        const nodes = moduleIds
          .map((id: string) => figma.getNodeById(id))
          .filter((n: BaseNode | null): n is SceneNode => n !== null);

        if (nodes.length > 0) {
          figma.currentPage.selection = nodes;
          figma.viewport.scrollAndZoomIntoView(nodes);
        }
        break;
      }

      case 'sync': {
        const { direction, syncText, syncImage, syncStyle } = msg;
        const options: SyncOptions = { syncText, syncImage, syncStyle };
        const selection = figma.currentPage.selection;

        if (selection.length === 0) {
          figma.notify('⚠️ 동기화할 요소를 선택해주세요');
          return;
        }

        const mapping = await loadMapping();
        let syncCount = 0;

        for (const node of selection) {
          const correspondingNode = await findCorrespondingNode(node, mapping);

          if (correspondingNode) {
            if (direction === 'pc-to-mobile' || direction === 'both') {
              syncCount += await syncContent(node, correspondingNode, options);
            }
            if (direction === 'mobile-to-pc' || direction === 'both') {
              syncCount += await syncContent(correspondingNode, node, options);
            }
          }
        }

        figma.notify(`✅ ${syncCount}개 항목 동기화 완료`);
        break;
      }

      case 'sync-all': {
        const { syncText, syncImage, syncStyle } = msg;
        const options: SyncOptions = { syncText, syncImage, syncStyle };

        const countPcToMobile = await syncAllModules(options, 'pc-to-mobile');
        figma.notify(`✅ 전체 페이지 동기화 완료 (${countPcToMobile}개 항목)`);
        break;
      }
    }
  } catch (error) {
    console.error(error);
    figma.notify(`❌ 오류: ${error instanceof Error ? error.message : '알 수 없는 오류'}`, {
      error: true
    });
  }
};

// 초기화 시 저장된 매핑 로드
loadMapping().then(mapping => {
  figma.ui.postMessage({
    type: 'mapping-loaded',
    mapping
  });
});
