# TODO - Enhanced AI Clothing Sorter

## Phase 1: Settings Caching Enhancement
- [ ] 1.1 Update `config.py` - Add more clothing types (polo, tank_top, leggings, cardigan, vest, romper, jumpsuit, etc.)
- [ ] 1.2 Update `src/path_cache.py` - Add more cached settings (use_gpu, copy_files)
- [ ] 1.3 Update `gui.py` - Load cached settings on startup

## Phase 2: New Detection Modules
- [ ] 2.1 Create `src/pattern_detector.py` - Pattern detection module (stripes, checks, floral, solid, etc.)
- [ ] 2.2 Create `src/size_detector.py` - Size/aspect ratio detection module

## Phase 3: Enhanced Classification
- [ ] 3.1 Update `src/classifier.py` - Improve classification with pattern and size detection
- [ ] 3.2 Update `src/similarity_matcher.py` - Enhanced sorting algorithm using pattern, size, looks

## Phase 4: Integration
- [ ] 4.1 Update `gui.py` - Integrate new pattern and size detection
- [ ] 4.2 Test and verify all changes work together
