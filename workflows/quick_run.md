## Quick Run（コピペ最小で回す）

### 目的
`人事/01VOICE` のファイル名を指定するだけで、`人事/02OUTPUT` にブログmdを作ります。

---

## 使い方（おすすめ）

CursorのChat/Agentに、**下の1行だけ**投げてください（`@`でファイル参照するのがポイントです）。

```text
@rules/blog_output_agent.md を守って、@人事/01VOICE/<ファイル名>.md からブログ記事を作成して。出力は 人事/02OUTPUT/YYMMDD_<タイトル>_agent.md（md形式）。トーンは @人事/02OUTPUT/260108_人類はどこにいくのか.md に寄せて。
```

例:

```text
@rules/blog_output_agent.md を守って、@人事/01VOICE/100人類はどこにいくのか.md からブログ記事を作成して。出力は 人事/02OUTPUT/260108_人類はどこへ向かうのか_agent.md（md形式）。トーンは @人事/02OUTPUT/260108_人類はどこにいくのか.md に寄せて。
```

---

## うまくいかない時
- 生成がブレる/短い/構成が崩れる場合は、`workflows/blog_from_voice.md` の「実行テンプレ（長文）」に切り替えてください。

