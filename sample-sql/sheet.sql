USE [pdf_db]
GO

/****** Object:  Table [dbo].[sheet]    Script Date: 9/6/2019 3:30:27 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[sheet](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_line] [int] NOT NULL,
	[SheetNum] [nvarchar](50) NULL,
	[Of_] [nvarchar](50) NULL,
	[Rev] [nvarchar](50) NULL,
	[DocClass] [nvarchar](50) NULL,
 CONSTRAINT [PK_sheet] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[sheet]  WITH CHECK ADD  CONSTRAINT [FK_sheet_Line] FOREIGN KEY([id_line])
REFERENCES [dbo].[Line] ([id])
GO

ALTER TABLE [dbo].[sheet] CHECK CONSTRAINT [FK_sheet_Line]
GO

